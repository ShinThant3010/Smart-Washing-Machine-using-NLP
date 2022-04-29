import stanza
import csv
import pandas as pd
import re
from datetime import datetime

# exctract MTC from the instructions
def get_MT(doc):
    verb_list = ['VB', 'VBP', 'VBG', 'VB']
    M = [] 
    T = []

    # ================================ GET M LIST ================================
    for i, sentence in enumerate(doc.sentences):
        for word in sentence.words:
            
            this_pair = [[],[]]
            
            if word.deprel == 'obj':

                id_obj = word.id
                obj = sentence.words[id_obj-1]
                id_headofobj = word.head
                
                if sentence.words[id_headofobj-1].xpos in verb_list or sentence.words[id_headofobj-1].upos in verb_list:
                    id_verb = id_headofobj
                    verb = sentence.words[id_verb-1]
                    # print(verb.text)
                    # print(obj.text)
                    this_pair[0].append(verb.lemma)
                    
                    j = id_obj - 1

                    while j >= 1 :
                        if sentence.words[j - 1].head == id_obj and sentence.words[j - 1].deprel == 'compound':
                            # print(sentence.words[j - 1].text)
                            this_pair[1].append(sentence.words[j - 1].lemma)
                        j = j-1
                    this_pair[1].append(obj.lemma)
                # print("===")
            M.append(this_pair)

    for i, sentence in enumerate(doc.sentences):
        for word in sentence.words:
            this_pair = [[],[]]
            if word.deprel == 'compound':
                id_mainnoun = word.head
                # print(sentence.words[id_mainnoun - 1].text)
                
                j = id_mainnoun - 1
                while j >= 1 :
                    if sentence.words[j - 1].head == id_mainnoun and sentence.words[j - 1].deprel == 'compound':
                        # print(sentence.words[j - 1].text)
                        this_pair[0].append(sentence.words[j - 1].lemma)
                    if sentence.words[j - 1].head == id_mainnoun and 'mod' in sentence.words[j - 1].deprel and 'nmod:poss' not in sentence.words[j - 1].deprel:
                        # print(sentence.words[j - 1].text)
                        this_pair[1].append(sentence.words[j - 1].lemma)
                    j = j-1
                this_pair[0].append(sentence.words[id_mainnoun - 1].lemma)
                # print("===")
            M.append(this_pair)

    for i, sentence in enumerate(doc.sentences):
        for word in sentence.words:
            this_pair = [[],[]]
            if ('mod' in word.deprel) and ('nmod:poss' not in word.deprel):
                id_mod = word.id
                mod = sentence.words[id_mod-1]
                id_main = word.head
                main = sentence.words[id_main-1]
                
                # print(mod.text)
                # print(main.text)
                this_pair[0].append(mod.lemma)
                this_pair[1].append(main.lemma)
                # print("===")
            M.append(this_pair)

    for i, sentence in enumerate(doc.sentences):
        for word in sentence.words:
            this_pair = [[],[]]
            if word.xpos in verb_list or word.upos in verb_list:
                if word.deprel == 'aux':
                    id_subverb = word.id
                    subverb = sentence.words[id_subverb-1]
                    if sentence.words[word.head - 1].xpos in verb_list or sentence.words[word.head - 1].upos in verb_list:
                        id_headofaux = word.head
                        headofaux = sentence.words[id_headofaux-1]
                        # print(subverb.text)
                        # print(headofaux.text)
                        this_pair[0].append(subverb.lemma)
                        this_pair[1].append(headofaux.lemma)
                        # print("===")
            M.append(this_pair)

    for i, sentence in enumerate(doc.sentences):
        for word in sentence.words:
            this_pair = [[],[]]
            if word.xpos in verb_list or word.upos in verb_list:
                if word.deprel == 'aux':
                    id_subverb = word.id
                    subverb = sentence.words[id_subverb-1]
                    if sentence.words[word.head - 1].xpos in verb_list or sentence.words[word.head - 1].upos in verb_list:
                        id_headofaux = word.head
                        headofaux = sentence.words[id_headofaux-1]

                        for word in sentence.words:                    
                            if word.deprel == 'advmod' and word.xpos == 'RB':
                                if word.head == id_headofaux:
                                    this_pair[0].append(subverb.lemma)
                                    this_pair[0].append(word.lemma)
                                    this_pair[1].append(headofaux.lemma)

                        for word in sentence.words:                    
                            if word.deprel == 'obj':
                                if word.head == id_headofaux:
                                    this_pair[1].append(word.lemma)

            M.append(this_pair)

    for i, sentence in enumerate(doc.sentences):
        for word in sentence.words:
            mod = None      
            this_pair = [[],[]]
            if word.deprel == 'case':
    #             print(word)
    #             print(sentence.words[word.head - 1].text)
                if sentence.words[word.head - 1].xpos == 'NN' and word.xpos == 'IN':
                    id_nn = word.head
                    id_adp = word.id
                    adp = word
                    nn = sentence.words[id_nn - 1]
                    
                    for word in sentence.words:
                        # find 'obj' dependency
                        if word.deprel == 'obl' and sentence.words[word.head - 1].xpos in verb_list:
                            id_verb = word.head
                            verb = sentence.words[word.head - 1]
                            # print("word", word.text)

                            word_id = word.id
                            k = word_id - 1
                            while k >= 1 :
                                if sentence.words[k - 1].head == word_id and 'mod' in sentence.words[k - 1].deprel and 'nmod:poss' not in sentence.words[k - 1].deprel:
                                    # print(sentence.words[k - 1].text)
                                    mod = sentence.words[k - 1]
                                k = k - 1
                            
                            for word in sentence.words:
                                if word.deprel == 'obj':
                                    if word.head == id_verb:
                                        obj = word
                                        id_obj = word.id

                                        j = id_obj - 1
                                        while j >= 1 :
                                            if sentence.words[j - 1].head == id_obj and sentence.words[j - 1].deprel == 'compound':
                                                this_pair[1].append(sentence.words[j - 1].lemma)
                                            
                                            j = j - 1
                                                            
                                        if mod != None:
                                            this_pair[1].append(mod.lemma)
                                        
                                        this_pair[1].append(nn.lemma)
                                        this_pair[1].append(obj.lemma)
                                        this_pair[0].append(verb.lemma)
                M.append(this_pair)


    for i, sentence in enumerate(doc.sentences):
        for word in sentence.words:
            this_pair = [[],[]]
            if word.deprel == 'cop' and word.xpos == 'VB' and sentence.words[word.head - 1].xpos == 'JJ':
                id_VB = word.id
                id_JJ = word.head

                this_pair[0].append(word.lemma)
                this_pair[1].append(sentence.words[id_JJ - 1].lemma)
            M.append(this_pair)

    # ================================ GET T LIST ================================
    for i, sentence in enumerate(doc.sentences):
        for word in sentence.words:                    
            if word.xpos == 'IN':
                id_in = word.id
                IN = word.lemma
                
                for word in sentence.words[id_in:]:
                    if word.xpos == 'CD':
                        id_cd = word.id
                        CD = word.lemma
                        
                        for word in sentence.words[id_cd:]:
                            if word.xpos == 'NN':
                                id_NN = word.id
                                NN = word.lemma

                                IN = (IN).replace('.', '')
                                CD = (CD).replace('.', '')
                                NN = (NN).replace('.', '')

                                T.append(IN)
                                T.append(CD)
                                T.append(NN)

    for i, sentence in enumerate(doc.sentences):
        for word in sentence.words:
            this_pair = [[],[]]
            if word.deprel == 'nummod':
                id_mod = word.id
                mod = sentence.words[id_mod-1]
                id_headofmod = word.head
                head = sentence.words[id_headofmod-1]
                this_pair[0].append((mod.lemma).replace('.', ''))
                this_pair[1].append((head.lemma).replace('.', ''))
            T.append(this_pair)

    M = [x for x in M if x!= [[],[]]]
    T = [x for x in T if x!= [[],[]]]
    M = [i for n, i in enumerate(M) if i not in M[:n]]
    T = [i for n, i in enumerate(T) if i not in T[:n]]

    return M, T
def set_cycle(flat_pair, fin_cycle, instruction):
    one_cycle_stem = ['normal', 'activewear', 'color', 'delic', 'handwash', 'favorit', 'steam',
                    'refresh', 'jean', 'duti', 'dirty', 'sanit', 'germ', 'white', 'quick']
    two_cycle_stem = [['fast', 'wash'], ['whitest', 'white'], ['heavi','duty'],  ['rins', 'spin'],
                        ['rins', 'cycl'], ['spin', 'cycl']]
    delicate_stem = ['nylon', 'silk', 'wool', 'cotton', 'linen', 'chiffon',
                    'georgett', 'moir', 'ninon']
    activewear_stem = ['gym', 'jogger', 'polyest', 'sport', 'tracksuit', 'leg',
                    'yoga', 'workout']
    color_stem = ['dye']
    cycle_dict = {
                    "normal": ['normal', None],
                    "activewear": ['activewear', 'gym', 'jogger', 'polyest', 'sport', 'tracksuit','leg', 'yoga', 'workout'],
                    "colors": ['dye', 'color'],
                    "fast_wash": ['fastwash', 'quick'],
                    "delicates": ['delicates','delic', 'nylon', 'silk', 'wool', 'cotton', 'linen', 'chiffon', 'georgett', 'moir', 'ninon'],
                    "hand_wash": ['handwash'],
                    "my_favorite": ['favorit'],
                    "steam_refresh": ['steam', 'refresh'],
                    "rinse&spin": ['rinsspin', 'rinscycl', 'spincycl', 'rinse&spin'],
                    "jeans": ['jean'],
                    "sanitize": ['sanit', 'germ'],
                    "heavy_duty": ['duti', 'dirty', 'heaviduty'],
                    "whitest_whites": ['white', 'whitestwhite']}
    set_cycle = None

    for delicate_fabric in delicate_stem:
        for word in flat_pair:
            u = re.search(delicate_fabric, word)
            if u != None:
                # print(x)
                set_cycle = 'delicates'

    for active_fabric in activewear_stem:
        for word in flat_pair:
            v = re.search(active_fabric, word)
            if v != None:
                # print(x)
                set_cycle = 'activewear'

    for color_fabric in color_stem:
        # print('yes')
        for word in flat_pair:
            w = re.search(color_fabric, word)
            # print(w)
            if w != None:
                # print(x)
                set_cycle = 'color'

    for (first_word, second_word) in two_cycle_stem:
        y_this_cycle = None
        z_this_cycle = None
        for word in flat_pair:
            y = re.search(first_word, word)
            if y != None:
                y_this_cycle = y
        for word in flat_pair:
            z = re.search(second_word, word)
            if z != None:
                z_this_cycle = z
        if y_this_cycle != None and z_this_cycle != None:
            set_cycle = first_word+second_word

    for cycle in one_cycle_stem:
        for word in flat_pair:
            x = re.search(cycle, word)
            if x != None:
                # print(x)
                set_cycle = cycle

    q = re.search('rinse and spin', instruction)
    if q != None:
        set_cycle = 'rinse&spin'


    no_this_cycle = None
    detergent_this_cycle = None
    for word in flat_pair:
        no = re.search('no', word)
        if no != None:
            no_this_cycle = no
    for word in flat_pair:
        detergent = re.search('detergent', word)
        if detergent != None:
            detergent_this_cycle = detergent
    if no_this_cycle != None and detergent_this_cycle != None:
        set_cycle = 'rinse&spin'

    for cycle in cycle_dict.keys():
        if set_cycle in cycle_dict[cycle]:
            fin_cycle = cycle

    if fin_cycle == None:
            fin_cycle = 'normal'

    return fin_cycle

def set_default_option(fin_cycle, temperature, spin_speed, soil_level):
    all_cycle = ["normal","activewear","colors","fast_wash","delicates",
                    "hand_wash","my_favorite","steam_refresh","rinse&spin","jeans","sanitize","heavy_duty","whitest_whites"]
    default_dict = {
        'temperature' : ['warm', 'warm', 'warm', 'warm', 'warm', 'warm', 'warm', 'hot', 'tap cold', 'cold', 'sanitize', 'warm', 'warm'],
        'spin_speed' : ['max','high', 'max', 'max', 'medium', 'low', 'max', 'no spin', 'max', 'medium', 'max', 'max', 'max'],
        'soil_level' : ['medium','medium','medium','extra light','medium','medium','medium','None','None','medium','medium','medium','medium']}

    idx = all_cycle.index(fin_cycle)
    temperature = default_dict['temperature'][idx]
    spin_speed = default_dict['spin_speed'][idx]
    soil_level = default_dict['soil_level'][idx]
    return temperature, spin_speed, soil_level

def set_temperature(flat_pair, temperature, instruction):
    temperature_stem = ['water', 'temperatur']
    temp_opt_stem = ['sanit', 'hot', 'warm', 'cold', 'tap']
    for temp_key in temperature_stem:
        for word in flat_pair:
            a = re.search(temp_key, word)
            if a != None:
                for temp_option in temp_opt_stem:
                    for word in flat_pair:
                        b = re.search(temp_option, word)
                        if b != None: 
                            temperature = b.group()
                            # print(b.string)
    if temperature == 'tap':
        temperature = 'tap cold'
    if temperature == 'cold' and 'tap' not in instruction:
        temperature = 'cold'
    if (temperature == 'cold') and ('tap' in instruction):
        temperature = 'tap cold'
    return temperature
def set_spinspeed(flat_pair, spin_speed):
    spin_stem = ['spin', 'speed']
    spin_opt_lem = ['max', 'high', 'medium', 'low', 'no']
    for spin_key in spin_stem:
        for word in flat_pair:
            a = re.search(spin_key, word)
            if a != None:
                for spin_option in spin_opt_lem:
                    for word in flat_pair:
                        b = re.search(spin_option, word)
                        if b != None: 
                            spin_speed = b.group()
                            # print(b.string)
    if spin_speed == 'no':
        spin_speed = 'no spin'
    return spin_speed
def set_soillevel(flat_pair, soil_level, instruction):
    soil_stem = ['soil', 'level']
    soil_opt_stem = ['max', 'heavy', 'heavi', 'medium', 'light', 'extra']
    for soil_key in soil_stem:
        for word in flat_pair:
            a = re.search(soil_key, word)
            if a != None:
                for soil_option in soil_opt_stem:
                    for word in flat_pair:
                        b = re.search(soil_option, word)
                        if b != None: 
                            soil_level = b.group()
                            # print(b.string)
    if soil_level == 'heavi':
        soil_level = 'heavy'
    if soil_level == 'extra':
        soil_level = 'extra light'
    if soil_level == 'light' and 'extra' not in instruction:
        soil_level = 'light'
    if (soil_level == 'light') and ('extra' in instruction):
        soil_level = 'extra light'
    return soil_level
def set_options(flat_pair, opt_list, option_fin, instruction):
    one_option_stem = ['wrinkl','control','lock','prewash','mute','sound', 'quiet', 'loud', 'nois', 'rins']
    two_option_stem = [['fresh', 'rins'], ['extra', 'rins']]
    option_dict = {
                    "fresh_rinse": ['fresh_rinse', 'rins'],
                    "prewash": ['prewash'],
                    "wrinkle_release": ['wrinkl'],
                    "control_lock": ['control','lock'],
                    "mute_sound": ['mute', 'sound', 'quiet', 'loud', 'nois']
                }
    for (first_word, second_word) in two_option_stem:
        y_this = None
        z_this = None
        for word in flat_pair:
            y = re.search(first_word, word)
            if y != None:
                y_this = y
        for word in flat_pair:
            z = re.search(second_word, word)
            if z != None:
                z_this = z
        if y_this != None and z_this != None:
            opt_list.append('fresh_rinse')

    for option in one_option_stem:
        for word in flat_pair:
            h = re.search(option, word)
            if h != None:
                # print(h.group())
                # print(x)
                opt_list.append(h.group())
                # print(h.string)

    q = re.search('wrinkl', instruction)
    if q != None:
        opt_list.append(q.group())

    for option in option_dict.keys():
        for opt_item in opt_list:
            if opt_item in option_dict[option]:
                option_fin[option] = True
    return option_fin

def check_condition(fin_cycle, temperature, spin_speed, soil_level, option_for_df):
    note = []
    conditions = [
    {'temperature' : ['sanitize', 'hot', 'warm', 'cold', 'tap cold'],
                    'spin_speed' :  ['max', 'high', 'medium', 'low', 'no spin'],
                    'soil_level' : ['max', 'heavy', 'medium', 'light', 'extra light'],
                    'option':  [True, True, True]
                }
    ,{'temperature' : ['warm', 'cold', 'tap cold'],
                    'spin_speed' :  ['high', 'medium', 'low'],
                    'soil_level' : ['medium', 'light', 'extra light'],
                    'option' :  [True, False, True]
                }
    ,{'temperature' : ['warm', 'cold', 'tap cold'],
                    'spin_speed' :  ['max', 'high', 'medium', 'low'],
                    'soil_level' : ['max', 'heavy', 'medium', 'light', 'extra light'],
                    'option' :  [True, False, True]
                }
    ,{'temperature' : ['warm', 'cold'],
                    'spin_speed':  ['max'],
                    'soil_level' : ['light', 'extra light'],
                    'option' :  [False, False, False]
                }
    ,{'temperature' : ['warm', 'cold', 'tap cold'],
                    'spin_speed' :  ['medium', 'low', 'no spin'],
                    'soil_level' : ['medium', 'light', 'extra light'],
                    'option' :  [True, False, True]
                }
    ,{'temperature' : ['warm'],
                    'spin_speed' :  ['low'],
                    'soil_level': ['medium'],
                    'option' :  [False, False, False]
                }
    ,{'temperature' : ['sanitize', 'hot', 'warm', 'cold', 'tap cold'],
                    'spin_speed' :  ['max', 'high', 'medium', 'low', 'no spin'],
                    'soil_level' : ['max', 'heavy', 'medium', 'light', 'extra light'],
                    'option' :  [True, True, True]
                }
    ,{'temperature' : ['hot'],
                    'spin_speed':  ['no spin'],
                    'soil_level': ['None'],
                    'option':  [False, False, False]
                }
    ,{'temperature' : ['tap cold'],
                    'spin_speed' :  ['max', 'high', 'medium', 'low', 'no spin'],
                    'soil_level' : ['None'],
                    'option' :  [True, False, False]
                }
    ,{'temperature' : ['cold'],
                    'spin_speed' :  ['medium'],
                    'soil_level' : ['medium'],
                    'option' :  [False, False, True]
                }
    ,{'temperature' : ['sanitize'],
                    'spin_speed' :  ['max', 'high'],
                    'soil_level' : ['max', 'heavy', 'medium'],
                    'option' :  [True, False, True]
                }
    ,{'temperature' : ['hot', 'warm', 'cold', 'tap cold'],
                    'spin_speed' :  ['max', 'high'],
                    'soil_level' : ['max', 'heavy', 'medium'],
                    'option' :  [True, True, True]
                }
    ,{'temperature' : ['hot', 'warm', 'cold', 'tap cold'],
                    'spin_speed' :  ['max', 'high', 'medium'],
                    'soil_level' : ['medium', 'light', 'extra light'],
                    'option' :  [True, True, True]
                }
    ]
    default_dict = {
        'default_temperature': ['warm', 'warm', 'warm', 'warm', 'warm', 'warm', 'warm', 'hot', 'tap cold', 'cold', 'sanitize', 'warm', 'warm'],
        'default_spin_speed' : ['max','high', 'max', 'max', 'medium', 'low', 'max', 'no spin', 'max', 'medium', 'max', 'max', 'max'],
        'default_soil_level' : ['medium','medium','medium','extra light','medium','medium','medium','None','None','medium','medium','medium','medium']}
    all_cycle = ["normal","activewear","colors","fast_wash","delicates",
                    "hand_wash","my_favorite","steam_refresh","rinse&spin","jeans","sanitize","heavy_duty","whitest_whites"]
    all_options = ["Fresh Rinse", "Prewash", "Wrinkle Release"]
    idx = all_cycle.index(fin_cycle)
    condition = conditions[idx]

    if temperature not in condition['temperature']:
        # print(default_dict['default_temperature'][idx])
        note.append(f"{temperature} water not available in {fin_cycle} cycle, Automatically changed to {default_dict['default_temperature'][idx]}." )
        temperature = default_dict['default_temperature'][idx]
    if spin_speed not in condition['spin_speed']:
        note.append(f"{spin_speed} spin speed not available in {fin_cycle} cycle, Automatically changed to {default_dict['default_spin_speed'][idx]}." )
        spin_speed = default_dict['default_spin_speed'][idx]
    if soil_level not in condition['soil_level']:
        # print(default_dict['default_soil_level'][idx])
        note.append(f"{soil_level} soil level not available in {fin_cycle} cycle, Automatically changed to {default_dict['default_soil_level'][idx]}." )
        soil_level = default_dict['default_soil_level'][idx]
    
    options = option_for_df[:3]
    for i in range(len(options)):
        if condition['option'][i] == False and options[i] == True:
            note.append(f"{all_options[i]} not available in {fin_cycle} cycle, Automatically cancelled {all_options[i]}.")
            option_for_df[i] = False
    return temperature, spin_speed, soil_level, option_for_df, note


def get_delay_time(after_hr, after_min):
    # print('hi')
    now = datetime.now()
    current_min = now.minute
    current_hr = now.hour
    
    ### Assume that user will not assign for yesterday and the day after tomorrow
    is_today = 1 
    is_am = 1 # is_am=0=pm, is_am=1=am

    set_min = current_min + after_min
    set_hr = current_hr + after_hr

    if set_min >= 60:
        set_hr += 1
        set_min = set_min % 60

    if set_hr >= 24:
        is_today = 0
        set_hr = set_hr - 24
    elif set_hr >= 12:
        is_am = 0
        set_hr = set_hr - 12
        
    if set_hr < 10:
        print_hr = '0' + str(set_hr)
    else:
        print_hr = str(set_hr)

    if set_min < 10:
        print_min = '0' + str(set_min)
    else:
        print_min = str(set_min)

    # Start at 01:30 am tomorrow.
    print_str = 'Start at ' + print_hr + ':' + print_min

    if is_am:
        print_str += ' am'
    else:
        print_str += ' pm'

    if is_today == 0:
        print_str += ' tomorrow.'
        
    return print_str
def is_today_fix (time, period):
    now = datetime.now()
    current_hr = now.hour
    is_today = 1
    
    if current_hr < 13:
        current_period = 'am'
    else:
        current_period = 'pm'
        current_hr = current_hr - 11
    if ':' in time:
        time = time.rpartition(':')[0]
        
    if ((current_period == period) and (current_hr > int(time))) or (current_period == 'pm' and period == 'am'):
        is_today = 0
    return is_today
def set_time(T):

    after_hr = 0
    after_min = 0
    time = None
    if 'half' in T:
        after_min = 30
    for item in T:
        if isinstance(item, list):
            first_part, second_part = item
            if any(c in second_part for c in ('hour', 'hours')):
                after_hr = int(first_part[0])
            if 'minute' in second_part:
                after_min = int(first_part[0])
            if any(c in second_part for c in ('am', 'pm')):
                time = first_part[0]
                period = second_part[0]
    if not time == None:
        if is_today_fix(time, period) == 1:
            time_str = 'Start at ' + time + ' ' + period + '.'
        else: 
            time_str = 'Start at ' + time + ' ' + period + ' tomorrow.'
    else:
        time_str = get_delay_time(after_hr, after_min)
    return time_str