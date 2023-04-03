import math
import time


class ProgressBar(object):
    # region поля класса
    _default_progress_size: int = 49
    current_progress: float
    total_progress: float
    bar_size: int = _default_progress_size
    caption: str

    textCritical: str = 'Превышение времени выполнения!'
    cWarning = '\033[93m'
    cCritical = '\033[91m'
    cNormal = '\033[0m'

    # endregion

    def setup(self, caption: str, total_progress: int = 0, current: int = 0, bar_size: int = _default_progress_size):
        self.current_progress = current
        self.total_progress = total_progress
        self.caption = caption
        if bar_size != self._default_progress_size:
            self.bar_size = bar_size

    def next(self, current: int = 0, caption: str = ''):
        # region настройка прогресс бара
        if current == 0:
            current = 1
        if caption == '':
            caption = self.caption
        self.current_progress += current
        bar_length_unit_value = (self.total_progress / self.bar_size)
        completed_bar_part = math.ceil(self.current_progress / bar_length_unit_value)
        if completed_bar_part > self.bar_size:
            completed_bar_part = self.bar_size
        completed = '*' * completed_bar_part
        remaining = ' ' * (self.bar_size - completed_bar_part)
        done = ((self.current_progress / self.total_progress) * 100)
        color = self.cNormal
        # endregion
        # region проверка превышения времени выполнения
        if done >= 200:
            done, color, caption = 100, self.cCritical, caption + ' ' + self.textCritical
        if done >= 110:
            done, color = 100, self.cWarning
        if done >= 100:
            done = 100
        # endregion
        print(color + '[{0}{1}] {2:6.2f}% {3}'.format(completed, remaining, done, caption), end=self.cNormal + '\r')

    def show_example(self):
        self.setup('Выполнение ...', 100)
        for i in range(0, 555):
            self.next()
            time.sleep(0.01)
        print()
