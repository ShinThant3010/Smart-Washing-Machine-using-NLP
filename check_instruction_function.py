#%%
import stanza
import csv
import pandas as pd
import re
from textblob import TextBlob
from functions import get_MT, set_cycle, set_default_option, set_temperature, set_spinspeed, set_soillevel, set_options, set_time, check_condition

nlp = stanza.Pipeline(lang='en', processors='tokenize, mwt, pos, lemma, depparse')

df = pd.DataFrame(data=None, index=None, 
        columns=['Sentence','M','T','Cycle','Temperature','Spin Speed','Soil Level','Options','Time','Note'])

f = open("test_instructions.csv")
for ix, row in enumerate(csv.reader(f)):
    instruction = row[0]
    instruction = instruction.lower()

    # # ======= SPELLING CORRECTION ======
    # instruction = TextBlob(instruction)
    # instruction = str(instruction.correct())

    doc = nlp(instruction)

    # ===================== GET MT ========================
    M , T = get_MT(doc)
    # =============================================================
    cycle_list = []
    fin_cycle = None
    temperature = None
    spin_speed = None
    soil_level = None
    opt_list = []
    option_fin = {
                "fresh_rinse": False,
                "prewash": False,
                "wrinkle_release": False,
                "control_lock": False,
                "mute_sound": False
            }
  
    for one_pair in M:
        flat_pair = []
        for subsublist in one_pair:
            for item in subsublist:
                flat_pair.append(item)
        
        # =============GET CYCLE & SET DEFAULT OPTIONS ================
        cycle_this_pair = set_cycle(flat_pair, fin_cycle, instruction)
        cycle_list.append(cycle_this_pair)
        # ======================== GET TEMPERATURE =====================
        temperature = set_temperature(flat_pair, temperature, instruction)
        # ======================== GET SPIN SPEED ======================
        spin_speed = set_spinspeed(flat_pair, spin_speed)
        # ======================== GET SOIL LEVEL ======================
        soil_level = set_soillevel(flat_pair, soil_level, instruction)
        # ======================== GET THE OPTIONS =====================
        option_fin = set_options(flat_pair, opt_list, option_fin, instruction)

    cycle_list = list(set(cycle_list))
    # print(cycle_list)
    if len(cycle_list) > 1:
        cycle_list.remove('normal')
        fin_cycle = cycle_list[0]
    if len(cycle_list) == 0:
        fin_cycle = 'normal'
    if len(cycle_list) == 1:
        fin_cycle = cycle_list[0]
    # print(fin_cycle)

    default_temperature, default_spin_speed, default_soil_level = set_default_option(fin_cycle, temperature, spin_speed, soil_level)

    if temperature == None :
        temperature = default_temperature
    if spin_speed == None :
        spin_speed = default_spin_speed
    if soil_level == None :
        soil_level = default_soil_level

    option_for_df = []  
    for option in option_fin.keys():
        option_for_df.append(option_fin[option])

    time_str = set_time(T)

    temperature, spin_speed, soil_level, option_for_df, note = check_condition(fin_cycle, temperature, spin_speed, soil_level, option_for_df)
    this_row = [instruction, M, T, fin_cycle, temperature, spin_speed, soil_level, option_for_df, time_str, note]
    
    df.loc[len(df)] = this_row

    
print(df.head())
df.to_csv('test_output.csv', index=False)
# %%
