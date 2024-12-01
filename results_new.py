import os
import sys

application_root_directory = os.environ['APP_HOME']
sys.path.append(application_root_directory)



import pickle
import matplotlib.pyplot as plt


#
# construct this filename from previous data
#
#history_file = application_root_directory + '/output/' + '57f47108-380d-4e78-aeb9-7ebccd07ec65----aafe0b89-98f1-47fc-9b9a-8008699fb807_final_history_regressor.pickled'

#history_file = application_root_directory + '/output/' + '57f47108-380d-4e78-aeb9-7ebccd07ec65----257c129f-9def-45dc-9c99-87f33f003a22_final_history_regressor.pickled'

#history_file = application_root_directory + '/output/' + '57f47108-380d-4e78-aeb9-7ebccd07ec65----fa5ed954-6c98-4fbf-907e-e8d23e77a206_final_history_regressor.pickled'

#
# no change in learning rate
#
history_file = application_root_directory + '/output/' + '57f47108-380d-4e78-aeb9-7ebccd07ec65----3384b0c6-3369-4a8d-8ce4-356b8c78e90f_final_history_regressor.pickled'

#
# change in learning rate
#
#history_file = application_root_directory + '/output/' + '57f47108-380d-4e78-aeb9-7ebccd07ec65----228d4a28-0ddd-4093-872f-182814381c0f_final_history_regressor.pickled'

#
# change in learning rate 10 epochs
#
history_file = application_root_directory + '/output/' + '57f47108-380d-4e78-aeb9-7ebccd07ec65----b90223c1-67b6-4f22-885c-584fb223b659_final_history_regressor.pickled'


with open(history_file, 'rb') as f:
    history = pickle.load(f)

if False:
    print(history['mse'])
    print()
    print(history['loss'])
    print()
    print(history['val_mse'])
    print()
    print(history['val_loss'])
    print()
    print(history['lr'])

#
# plot loss
#
#epochs = range(1, len(history['loss']) + 1)

n = 10

epochs = range(1, n)

plt.figure()
#plt.plot(epochs, history['loss'][0:(n - 1)], '-.', label='Loss')
#plt.plot(epochs, history['val_loss'][0:(n - 1)], '-.', label='Validation Loss')

plt.plot(epochs, history['mse'][0:(n - 1)], '-.', label='MSE')
plt.plot(epochs, history['val_mse'][0:(n - 1)], '-.', label='Validation MSE')

plt.legend()
plt.savefig(application_root_directory + '/output/' + 'test.png')
plt.close()

