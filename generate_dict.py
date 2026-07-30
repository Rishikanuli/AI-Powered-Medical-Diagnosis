import json

diseases = [
    ("Influenza", "Moderate Viral Infection", "Rest & Antivirals"),
    ("COVID-19", "Highly Contagious", "Isolate & Monitor"),
    ("Pneumonia", "Severe Respiratory", "Antibiotics & Care"),
    ("Tuberculosis", "Chronic Infectious", "Prolonged Antibiotics"),
    ("Dengue", "Acute Viral/Mosquito", "Vector Control & Fluids"),
    ("Malaria", "Severe Parasitic", "Urgent Antimalarials"),
    ("Typhoid", "Bacterial Enteric", "Antibiotics & Hydration"),
    ("Sepsis", "Life-Threatening Emergency", "Immediate Resuscitation"),
    ("Gastroenteritis", "Acute/Mild-Moderate", "Fluid Replacement"),
    ("Food Poisoning", "Acute/Moderate Risk", "Hydration Focus"),
    ("GERD", "Chronic/Manageable", "Dietary Modification"),
    ("Peptic Ulcer", "Acute/GI Risk", "GI Rest & Meds"),
    ("Gastritis", "Acute/Gastrointestinal", "Bland Diet & Antacids"),
    ("IBS", "Chronic/Discomfort", "Symptomatic Relief"),
    ("Crohn’s Disease", "Chronic Inflammatory", "Immunosuppressive Care"),
    ("Ulcerative Colitis", "Severe Inflammatory", "Specialist GI Consult"),
    ("Hepatitis", "Acute/Hepatic Risk", "Liver Function Monitor"),
    ("Cirrhosis", "End-Stage/Severe", "Urgent Hepatology Consult"),
    ("Pancreatitis", "Severe Abdominal", "ER/Possible Surgery"),
    ("Gallstones", "Acute Biliary", "Surgical Evaluation"),
    ("Diabetes", "Chronic/High Monitoring", "Strict Glycemic Control"),
    ("Hypoglycemia", "Metabolic Emergency", "Consume Fast Sugar"),
    ("Hyperthyroidism", "Endocrine Imbalance", "Endocrinologist Consult"),
    ("Hypothyroidism", "Chronic/Manageable", "Daily Hormone Therapy"),
    ("Addison’s Disease", "Severe Endocrine", "Steroid Replacement"),
    ("Cushing’s Syndrome", "Metabolic Excess", "Specialist Evaluation"),
    ("Electrolyte Imbalance", "Acute Metabolic", "IV Fluid Correction"),
    ("Dehydration", "Acute/Fluid Loss", "Aggressive Hydration"),
    ("Vitamin B12 Deficiency", "Nutritional Deficiency", "Dietary/Vitamin Supps"),
    ("Iron Deficiency Anemia", "Chronic/Nutritional", "Iron Supplementation"),
    ("Stroke", "Critical Neurological", "Urgent Stroke Protocol"),
    ("TIA", "Acute Neurological", "Immediate Neuro Eval"),
    ("Brain Tumor", "Severe Neurological", "Oncology/Neuro Consult"),
    ("Parkinson’s", "Chronic/Progressive", "Long-term Neuro Care"),
    ("Alzheimer’s", "Progressive Cognitive", "Supportive Care Plan"),
    ("Multiple Sclerosis", "Chronic Autoimmune", "Disease Modifying Rx"),
    ("Migraine", "Disabling/Moderate", "Dark Room & Meds"),
    ("Epilepsy", "Chronic Seizure Risk", "Neurology Management"),
    ("Vertigo Disorder", "Acute Vestibular", "Balance Therapy"),
    ("Concussion", "Acute/Trauma Risk", "Cognitive Rest"),
    ("Asthma", "Chronic/Acute Flare", "Use Rescue Inhaler"),
    ("COPD", "Chronic Respiratory", "Pulmonology Care"),
    ("Lung Cancer", "Oncological/High Risk", "Oncology Management"),
    ("Pulmonary Embolism", "Life-Threatening Clot", "Immediate ER Protocol"),
    ("Sinusitis", "Acute Respiratory", "Decongestants & Rest"),
    ("Allergic Rhinitis", "Mild Allergic/Low Risk", "Allergen Avoidance"),
    ("Bronchitis", "Acute/Chest Risk", "Symptomatic Rest"),
    ("Interstitial Lung Disease", "Progressive Pulmonary", "Specialist Pulmonology"),
    ("Bronchiectasis", "Chronic Lung Damage", "Airway Clearance"),
    ("COVID Pneumonia", "Severe Viral Complication", "Oxygen & Hospital Care"),

    # --- 50 New Diseases ---
    ("Appendicitis", "Severe Abdominal / ER Risk", "Immediate Surgical Consult"),
    ("Urinary Tract Infection (UTI)", "Acute Bacterial Infection", "Clinician Visit & Antibiotics"),
    ("Kidney Stones", "Acute Renal / Severe Pain", "Nephrology / ER Care"),
    ("Otitis Media", "Acute Otic Infection", "ENT / Pediatrician Consult"),
    ("Conjunctivitis", "Highly Contagious Ocular", "Ophthalmic Drops & Hygiene"),
    ("Anaphylaxis", "Life-Threatening Emergency", "Immediate Epinephrine Injection"),
    ("Gout", "Acute Arthritic Flare", "Anti-inflammatory Care"),
    ("Rheumatoid Arthritis", "Chronic Autoimmune Joint", "Rheumatologist Care"),
    ("Osteoarthritis", "Chronic Degenerative Joint", "Joint Mobility & Support"),
    ("Fibromyalgia", "Chronic Pain Disorder", "Multimodal Symptom Relief"),
    ("Meningitis", "Critical Neuro Emergency", "Immediate ER Assessment"),
    ("Lyme Disease", "Acute Vector Infection", "Immediate Antibiotics"),
    ("Mononucleosis", "Acute Viral Fatigue", "Symptomatic Care & Rest"),
    ("Chickenpox", "Highly Contagious Viral", "Antipruritic Care & Rest"),
    ("Shingles", "Acute Viral Rash", "Antiviral Rx & Pain Care"),
    ("Tonsillitis", "Acute Throat Infection", "Symptomatic Relief & Meds"),
    ("Strep Throat", "Acute Bacterial Throat", "Antibiotic Therapy & Care"),
    ("Laryngitis", "Acute Vocal Cord Inflam", "Strict Vocal Rest"),
    ("Otitis Externa", "Acute Swimmer's Ear", "Otic Antibiotic Drops"),
    ("Chronic Hypertension", "Chronic Cardiovascular", "Daily BP Control & Diet"),
    ("Coronary Artery Disease (CAD)", "Chronic Ischemic Risk", "Cardiologist Management"),
    ("Congestive Heart Failure (CHF)", "Severe Cardiovascular", "Strict Fluid/Weight Mon"),
    ("Atrial Fibrillation", "Chronic Arrhythmia Risk", "Rate & Anticoagulant Rx"),
    ("Deep Vein Thrombosis (DVT)", "Critical Vascular Risk", "ER Care & Anticoagulation"),
    ("Angina", "Acute Coronary / Chest Pain", "Cardiology Care / Nitros"),
    ("Pericarditis", "Acute Cardiac Inflamm", "NSAIDs & Cardiologist"),
    ("Celiac Disease", "Chronic Autoimmune GI", "Strict Gluten-Free Diet"),
    ("Diverticulitis", "Acute Colonic Inflam", "Antibiotics & Gut Rest"),
    ("Hemorrhoids", "Acute/Chronic GI Pain", "Symptomatic Care & Diet"),
    ("Lactose Intolerance", "Chronic GI Deficiency", "Lactose Avoidance & Enz"),
    ("Psoriasis", "Chronic Dermatological", "Topicals & Specialist Care"),
    ("Eczema", "Chronic/Acute Skin Care", "Aggressive Moisturization"),
    ("Urticaria (Hives)", "Acute Allergic Skin", "Oral Antihistamines"),
    ("Scabies", "Contagious Parasitic Skin", "Permethrin Topical Treatment"),
    ("Rosacea", "Chronic Vascular Skin", "Gentle Skin & Topicals"),
    ("Alopecia Areata", "Autoimmune Hair Loss", "Dermatologist Care"),
    ("Osteoporosis", "Chronic Bone Density", "Calcium, Vitamin D & Phys"),
    ("Polycystic Ovary Syndrome (PCOS)", "Chronic Endocrine Care", "Hormonal & Lifestyle Care"),
    ("Chronic Fatigue Syndrome", "Chronic Systemic/Neuro", "Pacing & Supportive Care"),
    ("Sleep Apnea", "Chronic Respiratory Sleep", "CPAP Therapy & Sleep Study"),
    ("Insomnia", "Chronic Sleep Disorder", "CBT-I & Sleep Hygiene"),
    ("Generalized Anxiety Disorder (GAD)", "Chronic Psychiatric", "Psychotherapy & Meds"),
    ("Major Depressive Disorder (MDD)", "Severe Psychiatric Risk", "Therapy & Antidepressants"),
    ("Panic Disorder", "Acute Psychiatric Flare", "Coping Skills & Meds"),
    ("Obsessive-Compulsive Disorder (OCD)", "Chronic Neuro-Psychiatric", "CBT & Exposure Therapy"),
    ("Vascular Dementia", "Severe Progressive Cognitive", "Neurology & Card Care"),
    ("Glaucoma", "Critical Ocular Emergency", "Daily Pressure-Lowering Drops"),
    ("Cataracts", "Progressive Visual Care", "Ophthalmology / Surgery"),
    ("Dry Eye Syndrome", "Chronic Ocular Discomfort", "Lubricating Drops & Care"),
    ("Restless Legs Syndrome (RLS)", "Chronic Sleep/Neuro Care", "Neurology & Iron Check")
]

TAILORED_GUIDELINES = {
    "Stroke": {
        "dos": ["Call emergency services (911/112) immediately", "Note the exact time symptoms first started", "Keep patient calm, warm, and lying down with head slightly elevated"],
        "donts": ["Do not give the patient food, drink, or medications", "Do not give aspirin (unless explicitly directed by a doctor)", "Do not allow the patient to sleep or drive themselves"]
    },
    "Asthma": {
        "dos": ["Use your rescue inhaler (albuterol) immediately", "Sit upright and try to remain calm to ease breathing", "Remove yourself from potential environmental triggers (dust, smoke, cold air)"],
        "donts": ["Do not lie down (this restricts chest expansion and airways)", "Do not ignore severe chest tightness or difficulty speaking", "Do not engage in physical exertion until breathing is fully stabilized"]
    },
    "Diabetes": {
        "dos": ["Check blood glucose levels immediately", "Maintain a balanced, low-glycemic eating schedule", "Take prescribed insulin or oral glucose-lowering medication as scheduled"],
        "donts": ["Do not skip scheduled meals or medication doses", "Do not consume high-sugar carbonated beverages or sweets", "Do not ignore slow-healing minor cuts or foot lesions"]
    },
    "Hypoglycemia": {
        "dos": ["Consume 15 grams of fast-acting sugar (fruit juice, regular soda, glucose tabs)", "Recheck blood glucose in 15 minutes (Rule of 15)", "Eat a complex carbohydrate and protein snack (crackers, bread) after recovery"],
        "donts": ["Do not inject insulin when blood sugar is already low", "Do not eat high-fat foods like chocolate (fat delays sugar absorption)", "Do not drive or operate heavy machinery during an episode"]
    },
    "Dehydration": {
        "dos": ["Sip Oral Rehydration Salts (ORS) or water slowly", "Rest in a cool, well-ventilated, or shaded space", "Monitor urine color (aim for a pale straw yellow or clear color)"],
        "donts": ["Do not gulp large quantities of plain water too rapidly", "Do not consume alcohol, strong coffee, or sugary energy drinks", "Do not ignore symptoms like dizziness, dry mouth, or rapid heart rate"]
    },
    "Migraine": {
        "dos": ["Rest in a dark, quiet, well-ventilated room", "Apply a cold or warm compress to your forehead or neck", "Take prescribed abortive medications at the first sign of aura or onset"],
        "donts": ["Do not look at bright phone, TV, or laptop screens", "Do not skip meals or disrupt your normal sleep schedule", "Do not consume strong caffeine or alcoholic triggers"]
    },
    "COVID-19": {
        "dos": ["Isolate immediately in a dedicated, well-ventilated room", "Monitor oxygen levels regularly with a pulse oximeter", "Stay hydrated, rest, and use acetaminophen for fever control"],
        "donts": ["Do not delay seeking emergency care if oxygen falls below 92%", "Do not self-medicate with unverified clinical therapeutics", "Do not leave isolation or gather in unmasked spaces"]
    },
    "COVID Pneumonia": {
        "dos": ["Isolate immediately in a dedicated, well-ventilated room", "Monitor oxygen levels regularly with a pulse oximeter", "Stay hydrated, rest, and use acetaminophen for fever control"],
        "donts": ["Do not delay seeking emergency care if oxygen falls below 92%", "Do not self-medicate with unverified clinical therapeutics", "Do not leave isolation or gather in unmasked spaces"]
    },
    "Hypertension Crisis": {
        "dos": ["Rest quietly for 5 minutes and repeat blood pressure reading", "Take your prescribed blood pressure medication immediately", "Seek immediate emergency services if chest pain, severe headache, or confusion occurs"],
        "donts": ["Do not engage in any physical activity or movement", "Do not consume caffeine, salt, or nicotine products", "Do not panic or stress (which further elevates blood pressure)"]
    },
    "Iron Deficiency Anemia": {
        "dos": ["Consume iron-rich foods (lean meats, leafy greens, legumes)", "Take iron supplements with Vitamin C (enhances absorption)", "Schedule a follow-up blood test to track hemoglobin levels"],
        "donts": ["Do not take iron supplements with calcium, tea, or coffee", "Do not ignore persistent severe fatigue or pale skin", "Do not exceed the recommended iron dosage without supervision"]
    },
    "Vitamin B12 Deficiency": {
        "dos": ["Include Vitamin B12 rich foods (fish, meat, poultry, eggs, milk) in your diet", "Take prescribed B12 oral supplements or schedule B12 injections", "Keep track of neurological symptoms (tingling, memory issues)"],
        "donts": ["Do not ignore persistent tingling in hands or feet", "Do not stop taking supplements without consulting your doctor", "Do not assume symptoms are just due to fatigue or aging"]
    },
    "Influenza": {
        "dos": ["Rest at home and isolate to prevent spreading the virus", "Stay well-hydrated with water, warm broths, or herbal teas", "Take fever-reducing medication (acetaminophen/ibuprofen) as needed"],
        "donts": ["Do not return to work or school until fever-free for at least 24 hours", "Do not ask for antibiotics (they are ineffective against viral influenza)", "Do not engage in strenuous physical activity or exercise"]
    },
    "Common Cold": {
        "dos": ["Stay hydrated by drinking water, juice, clear broth, or warm lemon water", "Get plenty of rest to help your body fight off the virus", "Use saline nasal sprays or drops to help relieve stuffiness"],
        "donts": ["Do not take antibiotics, as they do not work against viral colds", "Do not overexert yourself physically", "Do not smoke or expose yourself to secondhand smoke"]
    },
    "Pneumonia": {
        "dos": ["Take all prescribed antibiotics or medications exactly as directed", "Get plenty of rest and drink lots of fluids to loosen chest congestion", "Use a cool-mist humidifier or take a warm bath to help clear lungs"],
        "donts": ["Do not stop taking prescribed antibiotics early, even if you feel better", "Do not take cough suppressants without consulting a doctor (coughing clears mucus)", "Do not expose yourself to smoke or cold air"]
    },
    "Food Poisoning": {
        "dos": ["Let your stomach settle by avoiding solid foods for a few hours", "Stay hydrated by sipping water, diluted sports drinks, or ORS", "Gradually introduce bland foods like bananas, rice, applesauce, and toast"],
        "donts": ["Do not take anti-diarrheal medications without checking with a doctor (they delay clearing toxins)", "Do not consume dairy, caffeine, alcohol, nicotine, or fatty foods", "Do not try to force eating when nauseous"]
    },
    "Gastroenteritis": {
        "dos": ["Drink plenty of fluids in small, frequent sips to prevent dehydration", "Eat bland, easy-to-digest foods when ready", "Wash your hands frequently to prevent spreading the infection"],
        "donts": ["Do not take anti-diarrheal drugs without consulting a doctor", "Do not eat highly seasoned, fatty, sweet, or dairy foods", "Do not prepare food for others while you are symptomatic"]
    },

    # --- 50 New Guidelines ---
    "Appendicitis": {
        "dos": ["Seek emergency medical care immediately", "Rest quietly and avoid movement", "Keep track of exactly when pain started and its migration to the lower right abdomen"],
        "donts": ["Do not eat, drink, or consume fluids (needs NPO for potential surgery)", "Do not take laxatives or use enemas (can cause appendix rupture)", "Do not apply heat or hot packs to the abdomen"]
    },
    "Urinary Tract Infection (UTI)": {
        "dos": ["Drink plenty of water to help flush out bacteria", "Complete the full course of prescribed antibiotics", "Practice proper front-to-back hygiene"],
        "donts": ["Do not ignore burning or pain during urination", "Do not consume bladder irritants like caffeine, alcohol, or spicy food", "Do not delay urinating when the urge arises"]
    },
    "Kidney Stones": {
        "dos": ["Drink aggressive amounts of water (2-3 liters/day) to help pass the stone", "Take prescribed pain medications and muscle relaxants as directed", "Strain your urine to catch the stone for laboratory analysis"],
        "donts": ["Do not consume high-oxalate foods (like spinach, rhubarb, beets)", "Do not ignore signs of fever, chills, or inability to urinate (indicates obstruction/infection)", "Do not self-medicate with high-dose calcium supplements"]
    },
    "Otitis Media": {
        "dos": ["Apply a warm compress to the affected ear to relieve pain", "Administer pain-relieving ear drops or oral analgesics as prescribed", "Keep the ear clean and dry"],
        "donts": ["Do not insert cotton swabs, bobby pins, or sharp objects into the ear canal", "Do not allow water or soap to enter the ear during showers", "Do not ignore persistent fluid drainage or hearing loss"]
    },
    "Conjunctivitis": {
        "dos": ["Wash your hands thoroughly and frequently", "Use separate clean towels and pillowcases daily", "Apply cool or warm compresses to the eyes to reduce swelling"],
        "donts": ["Do not rub or touch your eyes", "Do not wear contact lenses until the infection is completely resolved", "Do not share eye makeup, eye drops, or sunglasses with others"]
    },
    "Anaphylaxis": {
        "dos": ["Administer an epinephrine auto-injector (EpiPen) immediately", "Call emergency services (911/112) without delay", "Lay the patient flat with their legs elevated, keeping them warm"],
        "donts": ["Do not give oral medications if the patient is struggling to breathe", "Do not wait to see if symptoms improve on their own", "Do not allow the patient to stand up or walk around"]
    },
    "Gout": {
        "dos": ["Elevate and rest the affected joint", "Apply ice packs wrapped in a towel for 15-20 minutes at a time", "Drink plenty of water to dilute uric acid in the body"],
        "donts": ["Do not consume purine-rich foods like red meat, shellfish, or beer", "Do not wear tight or restrictive footwear over the painful joint", "Do not stop long-term gout medications (like allopurinol) without consulting a doctor"]
    },
    "Rheumatoid Arthritis": {
        "dos": ["Engage in low-impact joint-friendly exercises like swimming or walking", "Apply warm baths or heating pads to ease morning joint stiffness", "Take prescribed disease-modifying antirheumatic drugs (DMARDs) consistently"],
        "donts": ["Do not push through severe joint pain during flare-ups", "Do not consume pro-inflammatory processed foods or high sugars", "Do not self-adjust steroid dosages without medical supervision"]
    },
    "Osteoarthritis": {
        "dos": ["Maintain a healthy body weight to reduce stress on weight-bearing joints", "Use supportive footwear or joint braces as recommended", "Keep active with gentle, structured physical therapy"],
        "donts": ["Do not engage in high-impact jumping or running if knee/hip joints are degraded", "Do not remain sedentary for prolonged periods (causes joint locking)", "Do not ignore sudden increases in swelling or localized warmth"]
    },
    "Fibromyalgia": {
        "dos": ["Establish a strict, calming sleep hygiene routine", "Practice gentle stress-reduction techniques like meditation, yoga, or deep breathing", "Engage in very gradual, low-impact daily exercise"],
        "donts": ["Do not overexert yourself physically on 'good days' (causes crash cycles)", "Do not consume high levels of caffeine or artificial sweeteners", "Do not isolate yourself from social support networks"]
    },
    "Meningitis": {
        "dos": ["Seek emergency hospital admission immediately", "Keep the patient in a quiet, dark, and calm environment while waiting", "Monitor neurological responsiveness and breathing closely"],
        "donts": ["Do not delay emergency care waiting for a rash to appear (rash is a late sign)", "Do not administer oral pain relievers that might mask diagnostic symptoms", "Do not expose others to salivary contact (extremely contagious)"]
    },
    "Lyme Disease": {
        "dos": ["Complete a full 14-21 day course of oral doxycycline as prescribed", "Note the date of the tick bite and take a photo of any bullseye rash", "Wear tick-repellent clothing and check for ticks after outdoor activities"],
        "donts": ["Do not crush a tick with your bare hands during removal (use fine-tipped tweezers)", "Do not leave tick mouthparts embedded in the skin", "Do not assume you are cured if the rash disappears without treatment"]
    },
    "Mononucleosis": {
        "dos": ["Get aggressive physical rest and avoid all heavy lifting", "Stay hydrated with water, herbal teas, or broths", "Use warm saline gargles to relieve severe throat discomfort"],
        "donts": ["Do not participate in contact sports or vigorous exercise (risk of spleen rupture)", "Do not share cups, utensils, or saliva with others (extremely contagious)", "Do not take amoxicillin or ampicillin (can cause a severe drug rash in mono patients)"]
    },
    "Chickenpox": {
        "dos": ["Apply calamine lotion or take cool colloidal oatmeal baths to relieve itching", "Keep fingernails trimmed short or wear mittens to prevent scratching", "Provide loose, breathable cotton clothing"],
        "donts": ["Do not give aspirin to children with chickenpox (associated with fatal Reye's Syndrome)", "Do not scratch the blisters (can lead to secondary bacterial infections and permanent scarring)", "Do not visit public spaces or interact with unvaccinated individuals"]
    },
    "Shingles": {
        "dos": ["Consult a doctor within 72 hours of rash onset to start antivirals", "Keep the rash clean, dry, and loosely covered with a sterile bandage", "Apply cool, wet compresses to the blistered area to soothe burning"],
        "donts": ["Do not scratch or pop the blisters", "Do not touch or expose the rash to pregnant women, infants, or immunocompromised individuals", "Do not use harsh soaps, perfumes, or heavy oils on the affected skin"]
    },
    "Tonsillitis": {
        "dos": ["Gargle warm saltwater several times a day to ease throat soreness", "Rest your voice and consume soft, cool foods like yogurt, ice cream, or broths", "Use a cool-mist humidifier in your room"],
        "donts": ["Do not force swallowing of hard, dry, or highly acidic foods", "Do not smoke or expose yourself to secondhand smoke", "Do not stop taking prescribed throat medications early"]
    },
    "Strep Throat": {
        "dos": ["Take your prescribed course of antibiotics to prevent rheumatic fever", "Replace your toothbrush 24 hours after starting antibiotics", "Stay home from work or school until you have been on antibiotics for 24 hours"],
        "donts": ["Do not attempt to scrape or wipe white patches from your tonsils", "Do not share food, drinks, or eating utensils with others", "Do not consume highly acidic juices or spicy foods"]
    },
    "Laryngitis": {
        "dos": ["Rest your voice completely—avoid speaking, and do not whisper (whispering strains vocal cords more)", "Inhale steam or use a personal steam inhaler to moisturize vocal cords", "Drink plenty of warm, caffeine-free liquids"],
        "donts": ["Do not clear your throat repeatedly (this causes harsh vocal cord impact)", "Do not whisper or attempt to shout or sing", "Do not consume decongestants, as they dry out the throat and vocal tract"]
    },
    "Otitis Externa": {
        "dos": ["Apply prescribed antibiotic ear drops exactly as directed", "Keep the ear completely dry—use earplugs or a shower cap when bathing", "Use a blow dryer on the lowest heat setting held away from the ear to dry the canal"],
        "donts": ["Do not swim or submerge your head under water until cleared by a doctor", "Do not scratch the inside of the ear with fingers, keys, or cotton swabs", "Do not wear earplugs or hearing aids while the ear is actively draining"]
    },
    "Chronic Hypertension": {
        "dos": ["Take your prescribed blood pressure medication daily at the same time", "Adhere to a low-sodium, heart-healthy diet (like the DASH diet)", "Engage in moderate aerobic exercise (e.g., 30 minutes of walking) daily"],
        "donts": ["Do not skip or suddenly discontinue blood pressure medications (can cause rebound hypertensive crisis)", "Do not consume excessive alcohol, sodium, or processed foods", "Do not use over-the-counter decongestants without checking (they raise blood pressure)"]
    },
    "Coronary Artery Disease (CAD)": {
        "dos": ["Eat a diet low in saturated fats, trans fats, and cholesterol", "Take your daily aspirin, beta-blockers, or statins exactly as directed", "Learn to recognize the signs of a heart attack and keep nitroglycerin close if prescribed"],
        "donts": ["Do not ignore chest tightness, pressure, or shortness of breath during mild exertion", "Do not smoke or use any tobacco/nicotine products", "Do not engage in sudden, highly intense physical strain without medical clearance"]
    },
    "Congestive Heart Failure (CHF)": {
        "dos": ["Weigh yourself every morning and report a sudden gain of 2-3 lbs in a day", "Adhere to strict daily fluid and sodium limits as directed by your cardiologist", "Elevate your legs when sitting to reduce lower extremity swelling"],
        "donts": ["Do not consume high-salt canned soups, processed meats, or salty snacks", "Do not ignore worsening shortness of breath, especially when lying flat in bed", "Do not skip your daily diuretic (water pill) medications"]
    },
    "Atrial Fibrillation": {
        "dos": ["Take your prescribed blood thinners (anticoagulants) consistently to prevent stroke", "Monitor your heart rate and pulse regularly", "Avoid stress, anxiety, and panic which can trigger episodes"],
        "donts": ["Do not consume high amounts of caffeine, energy drinks, or alcohol (triggers episodes)", "Do not ignore sudden episodes of dizziness, fainting, or chest discomfort", "Do not take herbal supplements like ginseng or St. John's Wort without consulting your cardiologist"]
    },
    "Deep Vein Thrombosis (DVT)": {
        "dos": ["Seek immediate emergency care if you develop sudden calf swelling, pain, or warmth", "Keep your leg elevated when resting to reduce swelling", "Wear fitted compression stockings if prescribed by a vascular specialist"],
        "donts": ["Do not massage, rub, or squeeze the painful calf/leg (can dislodge the clot and cause a fatal pulmonary embolism)", "Do not sit or stand still for long periods without moving your ankles and legs", "Do not perform strenuous leg exercises until cleared by your physician"]
    },
    "Angina": {
        "dos": ["Stop what you are doing, sit down, and rest immediately when chest pain starts", "Use your prescribed nitroglycerin spray or sublingual tablet under your tongue as directed", "Seek emergency services if pain persists for more than 5 minutes after resting/nitroglycerin"],
        "donts": ["Do not attempt to push through chest pain or walk it off", "Do not eat a heavy meal during or immediately after an episode", "Do not expose yourself to freezing cold air or sudden emotional stress (constricts arteries)"]
    },
    "Pericarditis": {
        "dos": ["Sit upright and lean forward slightly to ease the chest pain", "Take prescribed high-dose anti-inflammatories (NSAIDs/colchicine) exactly as directed", "Ensure complete physical rest to allow the heart lining to heal"],
        "donts": ["Do not lie flat on your back (greatly exacerbates the sharp chest pain)", "Do not engage in physical exercise or athletic training until fully cleared", "Do not ignore symptoms like swelling in legs or severe shortness of breath"]
    },
    "Celiac Disease": {
        "dos": ["Adhere to a strict, 100% lifetime gluten-free diet", "Read all food, medicine, and cosmetic labels carefully for hidden wheat, barley, or rye", "Use separate kitchen utensils and toasters to prevent cross-contact"],
        "donts": ["Do not consume standard bread, pasta, beer, or baked goods made with wheat", "Do not cheat on your diet, even for small amounts (microscopic gluten damages the small intestine)", "Do not assume food is safe because it is served at a high-end restaurant without double-checking"]
    },
    "Diverticulitis": {
        "dos": ["Switch to a clear liquid diet during an active acute flare-up to let your bowel rest", "Take all prescribed antibiotics exactly as directed", "Gradually introduce a high-fiber diet once the inflammation has completely resolved"],
        "donts": ["Do not consume solid or high-fiber foods during an active painful flare-up", "Do not strain during bowel movements (use a stool softener if recommended)", "Do not take pain relievers like ibuprofen or naproxen (can increase risk of bowel perforation)"]
    },
    "Hemorrhoids": {
        "dos": ["Eat a high-fiber diet and drink plenty of water to keep stools soft and easy to pass", "Take warm sitz baths for 15-20 minutes, 2-3 times a day", "Apply over-the-counter hydrocortisone creams or hazel wipes to relieve itching"],
        "donts": ["Do not strain or hold your breath during bowel movements", "Do not sit on the toilet for prolonged periods (e.g., reading or browsing your phone)", "Do not use dry, rough toilet paper (use wet wipes or a bidet instead)"]
    },
    "Lactose Intolerance": {
        "dos": ["Limit or avoid dairy foods like milk, cream, soft cheeses, and ice cream", "Take lactase enzyme supplements (Lactaid) immediately before consuming dairy products", "Choose lactose-free dairy or plant-based milks (almond, soy, oat)"],
        "donts": ["Do not consume large portions of dairy on an empty stomach", "Do not ignore hidden dairy ingredients in processed foods, baked goods, or sauces", "Do not completely cut out calcium—ensure alternative sources like leafy greens or fortified foods"]
    },
    "Psoriasis": {
        "dos": ["Moisturize your skin immediately after bathing to lock in hydration", "Apply prescribed corticosteroid or vitamin D creams exactly as directed", "Expose skin to short, controlled periods of natural sunlight"],
        "donts": ["Do not pick, scratch, or aggressively scrub psoriasis plaques (can trigger new lesions, known as Koebner phenomenon)", "Do not take hot, long showers which dry out the skin", "Do not ignore joint pain or stiffness, which can indicate psoriatic arthritis"]
    },
    "Eczema": {
        "dos": ["Apply thick, fragrance-free ointments or creams twice daily", "Take short, lukewarm baths or showers using mild, soap-free cleansers", "Wear soft, loose, breathable cotton clothing"],
        "donts": ["Do not scratch or rub the itchy skin (leads to secondary infection and skin thickening)", "Do not use heavily fragranced laundry detergents, fabric softeners, or soaps", "Do not let your skin get excessively sweaty or overheated"]
    },
    "Urticaria (Hives)": {
        "dos": ["Take non-drowsy over-the-counter antihistamines to control itching and swelling", "Apply cool, damp cloths to the hives to soothe the burning sensation", "Wear loose-fitting, smooth-textured clothing"],
        "donts": ["Do not scratch or vigorously rub the hives", "Do not take hot showers, baths, or enter saunas (heat releases more histamine)", "Do not expose skin to harsh sunlight or tight elastic bands"]
    },
    "Scabies": {
        "dos": ["Apply permethrin 5% cream to your entire body from the neck down and wash off after 8-14 hours", "Treat all household members and close contacts at the exact same time", "Wash all worn clothing, towels, and bedding in hot water and dry on high heat"],
        "donts": ["Do not scratch the intense itching (can lead to severe bacterial infections)", "Do not skip hard-to-reach areas like skin folds, between fingers, and under nails during treatment", "Do not return to work or school until 24 hours after completing the permethrin treatment"]
    },
    "Rosacea": {
        "dos": ["Apply broad-spectrum SPF 30+ sunscreen daily (sun exposure is a major trigger)", "Use highly gentle, soap-free cleansers and wash with lukewarm water", "Keep a journal to identify your personal triggers (e.g. spicy food, wind, stress)"],
        "donts": ["Do not consume hot beverages, spicy foods, alcohol, or red wine (causes severe flushing flares)", "Do not use harsh facial scrubs, astringents, or alcohol-based skin products", "Do not rub or massage your facial skin"]
    },
    "Alopecia Areata": {
        "dos": ["Protect bald patches on the scalp with sun-protective hats or sunscreen", "Explore treatment options like corticosteroid injections or topical minoxidil", "Seek emotional support or counseling to cope with the stress of hair loss"],
        "donts": ["Do not use harsh chemical dyes, perms, or heating irons on remaining hair", "Do not style hair in tight, pulling styles like braids or ponytails", "Do not buy expensive, unproven 'miracle hair growth' products from unverified sources"]
    },
    "Osteoporosis": {
        "dos": ["Ensure adequate intake of calcium and Vitamin D daily through diet or supplements", "Engage in weight-bearing exercises like walking or resistance training to strengthen bones", "Modify your home environment to eliminate fall hazards (throw rugs, poor lighting)"],
        "donts": ["Do not engage in high-impact jumping, heavy forward bending, or twisting motions", "Do not consume excessive amounts of alcohol, caffeine, or carbonated beverages", "Do not lift extremely heavy objects without proper body mechanics"]
    },
    "Polycystic Ovary Syndrome (PCOS)": {
        "dos": ["Maintain a balanced, low-glycemic, anti-inflammatory diet", "Engage in regular physical exercise to improve insulin sensitivity", "Take prescribed medications (e.g., birth control, metformin) exactly as directed"],
        "donts": ["Do not skip meals or consume diets high in refined sugars and simple carbs", "Do not ignore irregular or absent menstrual periods (increases risk of endometrial lining issues)", "Do not get discouraged by slow weight management—focus on consistency"]
    },
    "Chronic Fatigue Syndrome": {
        "dos": ["Practice daily structured activity pacing to stay within your energy limits", "Ensure a highly relaxing, consistent sleep routine", "Maintain a balanced, easily digestible, nutrient-dense diet"],
        "donts": ["Do not attempt to 'push through' fatigue (causes severe post-exertional malaise crashes)", "Do not engage in vigorous, high-intensity exercise programs", "Do not schedule multiple stressful activities in a single day"]
    },
    "Sleep Apnea": {
        "dos": ["Use your CPAP machine consistently every single night as prescribed", "Sleep on your side or stomach rather than on your back", "Avoid alcohol and sedatives, especially in the evening (they relax throat muscles)"],
        "donts": ["Do not sleep on your back (causes the tongue and throat tissues to collapse into the airway)", "Do not ignore daytime sleepiness, morning headaches, or loud snoring", "Do not drive or operate machinery if you feel fatigued or un-rested"]
    },
    "Insomnia": {
        "dos": ["Go to bed and wake up at the exact same time every single day (even weekends)", "Keep your bedroom dark, quiet, and cool (60-67F)", "Use your bed ONLY for sleep and intimacy"],
        "donts": ["Do not look at blue-light emitting phone, TV, or computer screens in bed", "Do not consume caffeine, nicotine, or heavy meals within 4-6 hours of bedtime", "Do not lie in bed awake for more than 20 minutes (get up and do a quiet activity)"]
    },
    "Generalized Anxiety Disorder (GAD)": {
        "dos": ["Practice daily relaxation techniques (deep breathing, progressive muscle relaxation)", "Limit caffeine and stimulant intake (they mimic and trigger physical panic symptoms)", "Engage in regular, structured physical exercise to burning off stress hormones"],
        "donts": ["Do not use alcohol or recreational substances to self-medicate anxiety symptoms", "Do not isolate yourself when feeling anxious or overwhelmed", "Do not catastrophize or dwell on negative 'what-if' scenarios"]
    },
    "Major Depressive Disorder (MDD)": {
        "dos": ["Attend scheduled therapy sessions (CBT) and take medications exactly as prescribed", "Stay connected with family, friends, or support groups", "Break large tasks down into tiny, easily manageable daily steps"],
        "donts": ["Do not isolate yourself in your room or cut off communications", "Do not make major life-changing decisions during a severe depressive episode", "Do not suddenly discontinue antidepressant medications (can cause severe withdrawal)"]
    },
    "Panic Disorder": {
        "dos": ["Practice slow, deep, diaphragmatic breathing during an active panic attack", "Remind yourself that panic attacks are temporary and not life-threatening", "Focus on a physical object in your surroundings to ground yourself"],
        "donts": ["Do not fight or resist the panic attack (this increases adrenaline—let it peak and pass)", "Do not flee the situation immediately if safe (teaches your brain that the environment is dangerous)", "Do not consume energy drinks, coffee, or decongestants"]
    },
    "Obsessive-Compulsive Disorder (OCD)": {
        "dos": ["Practice Exposure and Response Prevention (ERP) techniques as guided by your therapist", "Delay performing compulsions by a few minutes, gradually increasing the time", "Recognize that intrusive thoughts are just noise and do not define you"],
        "donts": ["Do not seek constant reassurance from family or friends (fuels the OCD loop)", "Do not attempt to actively suppress intrusive thoughts (causes them to return stronger)", "Do not structure your daily life around avoiding triggers"]
    },
    "Vascular Dementia": {
        "dos": ["Maintain tight control over cardiovascular factors (blood pressure, diabetes, cholesterol)", "Keep a highly structured daily routine with visual memory aids (calendars, checklists)", "Engage in daily cognitive exercises and social interactions"],
        "donts": ["Do not make sudden, drastic changes to the patient's home environment", "Do not argue with or aggressively correct the patient when they are confused", "Do not leave dangerous items (stoves, car keys, medications) accessible"]
    },
    "Glaucoma": {
        "dos": ["Apply your prescribed pressure-lowering eye drops daily without fail", "Attend all scheduled ophthalmologist visits to monitor optic nerve health", "Wear protective eyewear during sports or home improvement"],
        "donts": ["Do not rub your eyes, especially after applying drops", "Do not assume your eyes are fine because you have no pain or noticeable vision loss", "Do not double up on drops if you miss a dose"]
    },
    "Cataracts": {
        "dos": ["Wear UV-blocking sunglasses outdoors to slow cataract progression", "Ensure bright, direct lighting in your reading and work areas", "Update your lens prescription regularly and schedule surgical evaluation when ready"],
        "donts": ["Do not drive at night if you experience severe glare, halos around lights, or double vision", "Do not use eye drops that promise to dissolve cataracts (there are no drops that cure them)", "Do not delay surgery if cataracts are severely impacting your daily independence"]
    },
    "Dry Eye Syndrome": {
        "dos": ["Use preservative-free artificial tears frequently throughout the day", "Follow the 20-20-20 rule during screen use (look 20 feet away for 20 seconds every 20 minutes)", "Use a warm compress on your eyes daily to help release natural oils"],
        "donts": ["Do not let air from fans, air conditioners, or car vents blow directly onto your face", "Do not rub your dry eyes (causes corneal abrasion)", "Do not wear contact lenses for prolonged hours without lubricating them"]
    },
    "Restless Legs Syndrome (RLS)": {
        "dos": ["Engage in regular, moderate exercise (like walking or yoga) in the morning or afternoon", "Take a warm bath or massage your leg muscles before bedtime", "Get your iron levels (ferritin) checked by your physician"],
        "donts": ["Do not perform intense, strenuous workouts close to bedtime (triggers RLS)", "Do not consume alcohol, caffeine, or nicotine in the evening", "Do not ignore symptoms—there are effective prescription medications available"]
    }
}

DEFAULT_DOS = ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"]
DEFAULT_DONTS = ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]

dos_and_donts = {}
for d, sev, act in diseases:
    # Ensure variety of colors
    if "Emergency" in sev or "Severe" in sev or "Critical" in sev or "Life-Threatening" in sev:
        color = "danger"
    elif "Acute" in sev or "Moderate" in sev or "Contagious" in sev:
        color = "warning"
    else:
        color = ""
        
    # Get tailored guidelines or fall back to defaults
    disease_guide = TAILORED_GUIDELINES.get(d, {})
    dos = disease_guide.get("dos", DEFAULT_DOS)
    donts = disease_guide.get("donts", DEFAULT_DONTS)
        
    dos_and_donts[d] = {
        "severity": sev,
        "severity_color": color,
        "action": act,
        "dos": dos,
        "donts": donts
    }

with open('new_dict.txt', 'w', encoding='utf-8') as f:
    f.write('DOS_AND_DONTS = {\n')
    for k, v in dos_and_donts.items():
        f.write(f'    "{k}": {json.dumps(v)},\n')
    f.write('}\n')
