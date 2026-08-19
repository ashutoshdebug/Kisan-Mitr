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

            =================================================================
            CROP PATHOLOGY CONTEXT & FIELD PARAMETER SCHEMA
            =================================================================

            You are an expert plant pathologist and precision agronomist.

            Analyze the following crop details, environmental data, and
            observed symptoms to determine the most likely crop disease and
            formulate an actionable Integrated Pest Management (IPM) plan.

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


            =================================================================
            REQUIRED ANALYSIS
            =================================================================

            1. PRIMARY DIAGNOSIS

            Determine:
            - Pathogen common name
            - Pathogen scientific name
            - Disease classification
            - Environmental trigger


            2. CHEMICAL CONTROL

            Determine:
            - Recommended active ingredients
            - Commercial/trade names where appropriate
            - Dosage and dilution rate
            - Spray/application guidelines
            - Pre-harvest interval if known


            3. BIOLOGICAL & ORGANIC ALTERNATIVES

            Determine:
            - Biological control agents
            - Organic spray options
            - Dosage
            - Application frequency
            - Soil/foliar application procedure


            4. CULTURAL & FIELD REMEDIATION

            Determine:
            - Irrigation adjustments
            - Field sanitation
            - Pruning/removal of infected material
            - Soil drainage and aeration
            - Other relevant cultural practices


            5. RECOVERY & FOLLOW-UP

            Determine:
            - Recommended foliar nutrition
            - Relevant micronutrients
            - Monitoring milestones
            - Expected follow-up period
            - Conditions requiring secondary treatment


            =================================================================
            OUTPUT REQUIREMENTS
            =================================================================

            Return the result ONLY as valid JSON.

            Do NOT include:
            - Markdown
            - Code fences
            - ```json
            - Explanations outside the JSON
            - Introductory text
            - Conclusions outside the JSON

            The JSON must follow EXACTLY this structure:

            {{
                "primary_diagnosis": {{
                    "pathogen_common_name": "",
                    "pathogen_scientific_name": "",
                    "disease_classification": "",
                    "environmental_trigger": ""
                }},

                "chemical_control": {{
                    "active_ingredients": [],
                    "trade_names": [],
                    "dosage": "",
                    "spray_guidelines": "",
                    "pre_harvest_interval": ""
                }},

                "biological_control": {{
                    "bio_control_agents": [],
                    "organic_sprays": [],
                    "application_frequency": "",
                    "application_procedure": ""
                }},

                "cultural_remediation": {{
                    "irrigation_adjustments": "",
                    "field_sanitation": "",
                    "soil_drainage_and_aeration": ""
                }},

                "recovery_followup": {{
                    "foliar_nutrition": [],
                    "micronutrients": [],
                    "monitoring_milestones": "",
                    "followup_period": "",
                    "secondary_treatment_conditions": ""
                }}
            }}

            IMPORTANT:
            - Return ONLY valid JSON.
            - Do not add Markdown formatting.
            - Do not add comments.
            - Do not change the JSON keys.
            - If information is unavailable, use an empty string or empty array.
        """
        print(self.prompt)

        return self.prompt
