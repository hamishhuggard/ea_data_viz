from plots.scatter import Scatter
from collections import Counter

class Wilkinson(Scatter):

    def __init__(
        self,
        df,
        value='value',
        bins=20,
        text=None,
        log_y=False,
        **kwargs,
    ):

        min_val = df[value].min()
        max_val = df[value].max()
        delta = (max_val - min_val) / bins

        def bin_value(value):
            num_deltas = round( (value - min_val) / delta )
            return min_val + delta * (num_deltas + 0.5)

        bin_col = f'{value}_bin'
        df[bin_col] = df[value].apply(bin_value)

        bin_counter = Counter()
        def get_count(value):
            bin_counter[value] += 1
            return bin_counter[value]
        count_col = f'{value}_count'
        df[count_col] = df[bin_col].apply(get_count)

        def get_text(row):
            bin_value = row[bin_col]
            row_count = row[count_col]
            # if this is the last row in the bin, return the text
            if row_count < 3 and row_count == bin_counter[bin_value]:
                display_text = row[text]
                max_text_len = 40
                if len(display_text) > max_text_len:
                    display_text = display_text[:max_text_len] + '...'
                return display_text
            # otherwise return an empty string
            else:
                return ''

        if text:
            text_col = f'{value}_text'
            df[text_col] = df.apply(get_text, axis=1)
        else:
            text_col = None

        super().__init__(
            df = df,
            y = bin_col,
            x = count_col,
            text = text_col,
            **kwargs,
        )
