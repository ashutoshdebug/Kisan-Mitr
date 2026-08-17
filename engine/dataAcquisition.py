class dataAcquision:
    def __init__(self):
        self.prompt = None

    def allFields(self, location, crop_season, temperature, humidity, rainfall, windspeed, variety, irrigation, soil, symptoms):
        self.prompt = f"""
            ================================================================================
            CROP PATHOLOGY CONTEXT & FIELD PARAMETER SCHEMA
            ================================================================================
            This multi-modal payload combines visual inspection with telemetry data to assess 
            crop pathology, rule out abiotic stress, and formulate an actionable IPM plan:

            - Location       : Region/district (determines endemic disease zones & microclimates).
            - Crop Season    : Kharif, Rabi, Zaid, or Perennial (identifies seasonal pathogen cycles).
            - Temperature    : Ambient temperature (drives sporulation/incubation rates).
            - Humidity       : Relative humidity (high RH >80% accelerates fungal infection).
            - Rainfall       : Precipitation volume (indicates root waterlogging or splash spread).
            - Windspeed      : Ambient wind velocity (indicates spore dispersal vector dynamics).
            - Variety        : Cultivar/hybrid strain (identifies genetic susceptibility).
            - Irrigation     : Method (Drip, Sprinkler, Rainfed - overhead spray raises canopy moisture).
            - Soil Type      : Edaphic profile (determines drainage, aeration, and root rot risk).
            - Symptoms       : Farmer-reported visual abnormalities (lesions, wilting, curling).
            - Image Asset    : Macro/canopy photograph processed by the visual detection model.

            ================================================================================
            EXPERT PATHOLOGIST PROMPT TEMPLATE
            ================================================================================
            You are an expert plant pathologist and precision agronomist. Analyze the following 
            crop details, field environment data, and visual diagnostic inference to prescribe 
            a comprehensive Integrated Pest Management (IPM) solution.

            ### INPUT DATA:
            - Location: {location}
            - Crop Season: {crop_season}
            - Temperature: {temperature}
            - Humidity: {humidity}
            - Rainfall: {rainfall}
            - Windspeed: {windspeed}
            - Crop Variety: {variety}
            - Irrigation Type: {irrigation}
            - Soil Type: {soil}
            - Observed Symptoms: {symptoms}

            ---

            ### INSTRUCTIONS:
            Generate a clear, actionable prescription containing:

            1. PRIMARY DIAGNOSIS:
            - Pathogen Name (Common and Scientific name).
            - Disease Classification (Fungal, Bacterial, Viral, or Abiotic Stress).
            - Environmental Trigger (How current temperature, humidity, rainfall, and irrigation exacerbated this disease).

            2. CHEMICAL CONTROL (CURATIVE):
            - Recommended Active Ingredients & Formulations (e.g., Azoxystrobin + Difenoconazole, Mancozeb, Copper Oxychloride).
            - Standard Commercial/Trade Names.
            - Exact Dosage & Dilution Rate (e.g., ml/g per liter of water and per acre).
            - Spray Guidelines (Foliar coverage, best time of day, safety gear, and Pre-Harvest Interval / PHI).

            3. BIOLOGICAL & ORGANIC ALTERNATIVES:
            - Bio-control Agents (e.g., Trichoderma viride, Bacillus subtilis, Pseudomonas fluorescens).
            - Organic Sprays & Dosages (e.g., Cold-pressed Neem oil 10,000 PPM @ 3ml/L).
            - Application frequency and soil/foliar application steps.

            4. CULTURAL & FIELD REMEDIATION:
            - Irrigation Adjustments (Modifications to watering schedule or switching from overhead to root-zone).
            - Field Sanitation (Pruning, destroying infected foliage, sterilizing farm tools).
            - Aeration & Soil Drainage (Spacing adjustments, weeding, improving soil percolation).

            5. RECOVERY & FOLLOW-UP (14-30 DAYS):
            - Foliar Nutrition & Micronutrients to build systemic resistance (e.g., Potassium phosphite, Zinc, Boron).
            - Monitoring milestones to assess whether a secondary treatment is required.
        """
        print(self.prompt)

        return self.prompt
