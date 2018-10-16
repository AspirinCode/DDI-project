from load_data_ddi import load_data
from model import CNN, MCCNN, BILSTM

########### Hyperparameter ###########
# 1. Training settings
train_mode = 'cnn'
nb_epoch = 10
batch_size = 200
learning_rate = 0.001
optimizer = 'adam'
use_pretrained = False

# 2. CNN specific
kernel_lst = [3, 4, 5]  # [3, 4, 5]
nb_filters = 200

# 3. RNN specific
rnn_dim = 300  # Dimension for output of LSTM

# 4. Model common settings
emb_dim = 300
pos_dim = 10
max_sent_len = 150
num_classes = 5
unk_limit = 8000
dropout_rate = 0.5

# 5. Self attention
use_self_att = False
######################################


if __name__ == '__main__':
    (tr_sentences2idx, tr_entity_pos_lst, tr_y), (te_sentences2idx, te_entity_pos_lst, te_y), \
        (vocb, vocb_inv), (tr_sentences, tr_drug1_lst, tr_drug2_lst, tr_rel_lst), (te_sentences,
                                                                                   te_drug1_lst, te_drug2_lst, te_rel_lst) = load_data(unk_limit=unk_limit, max_sent_len=max_sent_len)
    if train_mode.lower() == 'cnn':
        model = CNN(max_sent_len=max_sent_len,
                    vocb=vocb,
                    emb_dim=emb_dim,
                    pos_dim=pos_dim,
                    kernel_lst=kernel_lst,
                    nb_filters=nb_filters,
                    dropout_rate=dropout_rate,
                    optimizer=optimizer,
                    non_static=True,
                    lr_rate=learning_rate,
                    use_pretrained=use_pretrained,
                    unk_limit=unk_limit,
                    num_classes=num_classes)

    elif train_mode.lower() == 'mccnn':
        model = MCCNN(max_sent_len=max_sent_len,
                      vocb=vocb,
                      emb_dim=emb_dim,
                      pos_dim=pos_dim,
                      kernel_lst=kernel_lst,
                      nb_filters=nb_filters,
                      dropout_rate=dropout_rate,
                      optimizer=optimizer,
                      lr_rate=learning_rate,
                      use_pretrained=use_pretrained,
                      unk_limit=unk_limit,
                      num_classes=num_classes)

    elif train_mode.lower() == 'rnn':
        model = BILSTM(max_sent_len=max_sent_len,
                       vocb=vocb,
                       emb_dim=emb_dim,
                       pos_dim=pos_dim,
                       rnn_dim=rnn_dim,
                       dropout_rate=dropout_rate,
                       optimizer=optimizer,
                       non_static=True,
                       lr_rate=learning_rate,
                       use_pretrained=use_pretrained,
                       unk_limit=unk_limit,
                       num_classes=num_classes,
                       use_self_att=use_self_att)

    else:
        raise Exception("Wrong Training Model")
    model.show_model_summary()
    model.save_model()
    model.train(sentence=tr_sentences2idx, pos_lst=tr_entity_pos_lst, y=tr_y, nb_epoch=nb_epoch, batch_size=batch_size, validation_split=0.1)
    model.evaluate(sentence=te_sentences2idx, pos_lst=te_entity_pos_lst, y=te_y, batch_size=batch_size)
