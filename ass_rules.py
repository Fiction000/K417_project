from pymining import itemmining, assocrules, perftesting
from pymining import seqmining
from pymining import itemmining

transactions = []
with open('transaction_data.dat') as f:
    transactions.append(f.readline().split(' '))

relim_input = itemmining.get_relim_input(transactions)
report = itemmining.relim(relim_input, min_support=2)

freq_seqs = seqmining.freq_seq_enum(transactions, 2)
print(freq_seqs)
