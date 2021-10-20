from utils.plots.scatter import Scatter
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

        def trim_text(text, max_len):
            if len(text) < max_len:
                return text
            return text[:max_len-3] + '...'

        def get_text(row):
            bin_value = row[bin_col]
            row_count = row[count_col]
            display_text = row[text]
            # if the dot is in a row by itself then show its text
            if row_count == 1 and bin_counter[bin_value] == 1:
                return trim_text(display_text, 40)
            # if there are two dots in a row, show both of their text
            elif row_count == 2 and bin_counter[bin_value] == 2:
                other_text = df.loc[ (df[bin_col]==bin_value) & (df[count_col]==1), text ].iat[0]
                return trim_text(other_text, 20) + ', ' + trim_text(display_text, 20)
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
            transparent = False,
            **kwargs,
        )
