# Returns all co-changes that have a matching smell. Note: can contain duplicates.
import pandas as pd


class JoinHelper:
    @staticmethod
    def perform_chunkified_pair_join(df1, df2, level='file', compare_dates=True):
        chunks1 = split_into_chunks(df1, 60000)  # df's with <= 1000 rows
        chunks2 = split_into_chunks(df2, 60000)
        processed_chunks = []
        for cc_chunk in chunks1:
            for smell_chunk in chunks2:
                match_chunk = cc_chunk.merge(smell_chunk, how='inner', left_on=[level + '1', level + '2'],
                                             right_on=[level + '1', level + '2'])
                test_frame = match_chunk.head(5)
                test_smells = smell_chunk.head(5)
                test_cc = cc_chunk.head(5)
                # Check we at least have a match
                if len(match_chunk.index) == 0:
                    continue

                if compare_dates:
                    match_chunk = match_chunk[match_chunk['parsedStartDate'] <= match_chunk['parsedVersionDate']]
                    match_chunk = match_chunk[match_chunk['parsedVersionDate'] <= match_chunk['parsedEndDate']]

                    if len(match_chunk.index) == 0:
                        continue

                processed_chunks.append(match_chunk)
        del chunks1
        del chunks2
        return pd.concat(processed_chunks) if processed_chunks != [] else pd.DataFrame(
            columns=[level + '1', level + '2'])  # Note: do not add more columns here, since it results in duplicates during joins and thus columns like parsedDate_x

def split_into_chunks(df, chunk_size):
    return [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]