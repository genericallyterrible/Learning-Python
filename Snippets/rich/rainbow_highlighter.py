import inspect
import math
import os
from colorsys import hsv_to_rgb
from multiprocessing import Pool
from random import uniform
import time
from typing import Optional
from click import progressbar

from rich import print
from rich.console import Console
from rich.containers import Lines
from rich.highlighter import Highlighter
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.text import Text


class RainbowHighlighter(Highlighter):
    def __init__(
        self,
        hue: Optional[float] = None,
        char_step: float = -0.015,
        row_step: float = -0.03,
        console: Optional[Console] = None,
        progressbar: Optional[Progress] = None,
        task_id: Optional[TaskID] = None,
    ) -> None:
        super().__init__()
        if hue is None:
            self.hue = uniform(0, 1)
        else:
            self.hue = hue
        self.char_step = char_step
        self.row_step = row_step
        self.console = console
        self.progressbar = progressbar
        self.task_id = task_id

    @staticmethod
    def next_hue(hue, step_size: float) -> float:
        if math.isfinite(step_size):
            return (hue + step_size) % 1.0
        else:
            return uniform(0, 1)

    @staticmethod
    def highlight_row(hue, text, char_step) -> Text:
        # Stylize each character
        for index in range(len(text)):
            (r, g, b) = hsv_to_rgb(hue, 1.0, 1.0)
            text.stylize(
                f"rgb({int(r*255)},{int(g*255)},{int(b*255)})", index, index + 1
            )
            hue = RainbowHighlighter.next_hue(hue, char_step)
        return text

    @staticmethod
    def multiprocess(n_chars, n_lines) -> bool:
        cores = os.cpu_count()
        if cores is None or n_chars < 500_000 or n_lines <= 2:
            return False
        elif cores >= 6 or (cores >= 4 and n_chars > 3_000_000):
            return True
        else:
            return False

    def highlight_series(self, lines: Lines) -> Lines:
        for line in lines:
            line = RainbowHighlighter.highlight_row(self.hue, line, self.char_step)
            self.hue = self.next_hue(self.hue, self.row_step)
            if self.progressbar is not None and self.task_id is not None:
                self.progressbar.advance(task_id)
        return lines

    def highlight_parallel(self, lines: Lines) -> Lines:
        params = list()
        for line in lines:
            params.append((self.hue, line, self.char_step))
            self.hue = self.next_hue(self.hue, self.row_step)
        with Pool() as pool:
            result = pool.starmap_async(self.highlight_row, params)
            
            if self.progressbar is not None and self.task_id is not None:
                n_tot = result._number_left
                if n_tot != 0:
                    self.progressbar.update(self.task_id, total=n_tot)
                    while True:
                        n_rem = result._number_left
                        n_comp = n_tot - n_rem
                        self.progressbar.update(self.task_id, completed=n_comp)

                        if result.ready():
                            break
                        else:
                            time.sleep(1)
                self.progressbar.update(self.task_id, total=1, completed=1)
            else:
                result.wait()
            return Lines(result.get())

    def highlight(self, text: Text) -> None:

        lines: Lines = Lines()
        if self.console is not None:
            # Wrap to the console
            lines = text.wrap(self.console, self.console.width)
        else:
            # Split on lines
            lines = text.split()

        if self.progressbar is not None and self.task_id is not None:
            self.progressbar.update(task_id=task_id, total=len(lines))

        if not self.multiprocess(len(text), len(lines)):
            if self.progressbar is not None and self.task_id is not None:
                desc = self.progressbar.tasks[task_id].description
                self.progressbar.update(self.task_id, description=f"{desc} (series)")
            lines = self.highlight_series(lines)
        else:
            if self.progressbar is not None and self.task_id is not None:
                desc = self.progressbar.tasks[task_id].description
                self.progressbar.update(self.task_id, description=f"{desc} (parallel)")
            lines = self.highlight_parallel(lines)

        joined = Text("\n").join(lines)
        text.plain = joined.plain
        text.spans = joined.spans


if __name__ == "__main__":
    console = Console()

    plain_str = (
        inspect.cleandoc(
            """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis aliquet tempor urna vitae porttitor. Donec aliquam sollicitudin rutrum. Nullam risus lacus, dapibus quis semper sit amet, posuere quis arcu. Praesent consectetur ipsum eros, eu imperdiet ipsum lacinia vel. In tempor porttitor euismod. Donec a eleifend mi. Nunc sit amet neque a elit iaculis maximus. Aliquam sagittis turpis nec velit ultrices imperdiet. Vivamus mi orci, hendrerit eu felis tincidunt, ultrices aliquam lectus. Maecenas iaculis ipsum id lorem sodales, et efficitur lorem maximus. Donec ut sem a dui porttitor molestie volutpat et augue. In vitae egestas sapien. Suspendisse non mattis lectus, eu eleifend est. Nullam a ligula ipsum. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Suspendisse eleifend vestibulum elit, nec porta lectus viverra efficitur. Nulla dapibus pulvinar metus non tristique. Etiam at nulla eu sem convallis consequat. In facilisis molestie libero sit amet lacinia. Vestibulum accumsan suscipit augue sed pellentesque. Maecenas molestie lacus eget sollicitudin hendrerit. Nullam metus neque, semper a consectetur vel, dapibus sit amet augue. Vestibulum ultrices lectus non ipsum condimentum maximus. Proin id maximus justo.
        Vestibulum lacinia neque in dolor porttitor mattis. Etiam consectetur augue ut quam laoreet, sit amet imperdiet purus efficitur. Maecenas auctor, ipsum in dictum lacinia, nisi magna porttitor nisl, ac eleifend mi enim id ante. Cras sollicitudin dapibus felis eu tincidunt. Pellentesque a pulvinar ex. Sed vehicula eros magna, in elementum massa blandit quis. Nullam non orci augue. Vivamus feugiat consectetur commodo.
        Vivamus a ligula augue. Fusce gravida massa eleifend ipsum scelerisque aliquam. Proin gravida aliquet sapien. Integer nec pulvinar enim. Donec condimentum tristique lobortis. Quisque gravida maximus nunc, sit amet feugiat lorem vulputate sit amet. In venenatis ut leo nec mattis. Maecenas vehicula malesuada mi sed luctus. Aliquam odio sem, ullamcorper non pharetra quis, lobortis at tellus. Vestibulum eu quam vel massa blandit luctus. Mauris faucibus nibh ut posuere feugiat. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.
        Maecenas vel ipsum volutpat, tempus massa eget, finibus odio. Vivamus vitae est at ipsum bibendum lacinia. Praesent sit amet blandit justo. Ut mollis purus ut dui euismod pellentesque. Aenean facilisis, arcu non mollis lobortis, diam massa lobortis justo, sit amet tincidunt nibh eros at ipsum. Sed eu aliquam nisl. Pellentesque massa tortor, scelerisque vitae sapien iaculis, maximus volutpat dolor. Nam vel ultricies quam. Proin eget elementum turpis.
        Sed ultrices, odio id volutpat congue, ligula neque congue nulla, et malesuada nibh eros a dolor. Praesent sed lacinia libero. Sed id ante nec ante varius feugiat. Nam accumsan tristique tellus, et dictum augue feugiat fringilla. Integer id mi at diam volutpat varius condimentum sit amet dolor. In vulputate, tellus quis imperdiet finibus, sem nunc sollicitudin neque, sit amet rhoncus tortor massa sed neque. Sed efficitur dolor ornare purus tempor vehicula. Duis et lorem ut lacus tristique placerat. Maecenas eu velit feugiat mauris tempus commodo. Vestibulum tincidunt iaculis tortor, sed faucibus mauris posuere vel. In sit amet dolor vel dolor finibus scelerisque vitae in purus. Proin porttitor purus eu sapien consequat, vitae scelerisque diam auctor. Integer ex elit, congue a arcu ut, vehicula aliquet neque. Duis pretium, arcu sed tincidunt luctus, quam odio scelerisque nisi, ac sodales velit lectus in eros.
        Maecenas vitae tristique sapien. Proin laoreet egestas dui, eu ullamcorper nunc posuere ut. Fusce posuere lacus odio. Nulla facilisi. Donec imperdiet, elit non tincidunt ultricies, velit mi convallis ligula, finibus iaculis est nisl sit amet velit. Fusce eget lobortis quam. In nunc mauris, consectetur ut luctus sit amet, tincidunt quis tellus. Mauris eget efficitur quam. Fusce sagittis efficitur ex sit amet ultrices. Duis tincidunt eros facilisis ligula pellentesque eleifend. Nam augue justo, congue sed orci in, pharetra sagittis elit. Sed mattis consequat mauris, quis hendrerit dolor cursus gravida. Curabitur varius ligula ac ultricies vehicula. Phasellus ut elementum enim.
        Quisque eu magna in felis consequat fermentum vitae ac dui. Ut viverra purus est, et feugiat augue malesuada ut. Aenean at lobortis purus. Pellentesque non ornare ipsum, et lobortis enim. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Etiam a est vitae ex bibendum efficitur. Phasellus venenatis dolor id rhoncus semper. Suspendisse auctor consequat tellus molestie porttitor. Nullam dolor metus, molestie eu nulla sed, interdum ultricies turpis. Nulla et hendrerit nunc. Maecenas scelerisque nunc lacinia consectetur dictum.
        Nam consectetur nec mauris vitae bibendum. Suspendisse consectetur vitae nisl in feugiat. Quisque at magna felis. Morbi ultrices ut est vel semper. Quisque maximus, nisi eu lobortis fermentum, quam purus tincidunt purus, in sagittis eros nibh ac lorem. Praesent tincidunt elit sed tempus hendrerit. In hac habitasse platea dictumst. Sed vitae arcu hendrerit, euismod urna et, faucibus ex. Pellentesque eget lobortis erat, sit amet consectetur massa. Ut feugiat efficitur rhoncus. Aliquam bibendum lorem a urna ullamcorper, quis semper nibh cursus. Phasellus non venenatis neque. Pellentesque lacinia felis nec erat ornare cursus.
        Quisque vel ligula sed lorem vulputate blandit. Sed suscipit libero id molestie finibus. Integer ac rutrum quam. Curabitur gravida nisi arcu, ut sollicitudin dolor volutpat sit amet. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Maecenas quis tincidunt nisl. Curabitur porta bibendum sapien eu commodo. Nulla pellentesque, mi sit amet molestie rutrum, augue leo iaculis risus, vel venenatis arcu massa quis nisl. 
    """
        )
        * 1500
    )
    plain_text = Text(plain_str)

    newline = "\n"
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        "Elapsed:",
        TimeElapsedColumn(),
        refresh_per_second=4,  # Slower updates
    ) as progress_bar:
        print(f"Characters: {len(plain_str)}\t Lines: {plain_str.count(newline)}")
        task_id = progress_bar.add_task("Colorizing...", total=None)
        rainbow = RainbowHighlighter(console=console, progressbar=progress_bar, task_id=task_id)
        rainbow(plain_str)
