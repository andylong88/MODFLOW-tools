import pickle
import flopy

model_ws = r"../" 
namfile = "SES_ss.nam"  # your name file

ml = flopy.modflow.Modflow.load(
    namfile,
    model_ws=model_ws,
    version="mfnwt",   # or "mf2k", "mfnwt", "mfusg"
    verbose=True,
    check=False         # often helpful to bypass strict checks
)

with open("SES_ss_model.pkl", "wb") as f:
    pickle.dump(ml, f)
