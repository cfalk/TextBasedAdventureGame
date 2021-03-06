from Lexicon import Lexicon
import time
import sys

CHARACTER_PRINT_DELAY = 0.02
LINE_PRINT_DELAY = 0.4


class IoDevice:
    def __init__(self):
        self.lex = Lexicon()

    def input(self, translate_id=None, *formatArgs, force_type=str):
        while (True):
            try:
                if translate_id:
                    delay_print(self.lex.get(translate_id).format(*formatArgs))

                input_prefix = self.lex.get("STANDARD_INPUT_PREFIX")
                return force_type(input(input_prefix))
            except Exception as e:
                print("DEBUG-IO:{}".format(e))
                self.out("INVALID_INPUT_WARNING")

    def out(self, translate_id, prefix="", raw_kwargs=None, kwargs_to_translate=None):
        # Translate any kwargs that need to be translated using the Lexicon
        raw_kwargs = raw_kwargs or {}
        kwargs_to_translate = kwargs_to_translate or {}
        format_kwargs = {k: self.lex.get(arg) for k, arg in kwargs_to_translate.items()}
        format_kwargs.update(raw_kwargs)
    
        output = "{}{}".format(prefix, self.lex.get(translate_id).format(**format_kwargs))
        delay_print(output)


def delay_print(output):
    for char in output:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(CHARACTER_PRINT_DELAY)
    time.sleep(LINE_PRINT_DELAY)
    print()


IO = IoDevice()