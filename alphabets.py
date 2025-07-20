TN_LPR = dict(
    TN_ALPHABET='تونس',
    FA_DIGITS='0123456789'
)

ALPHABETS = {
    'TN_LPR': "".join(TN_LPR.values())
}


ALPHABETS = {k: "".join(list(v.values())) for k, v in ALPHABETS.items()}
