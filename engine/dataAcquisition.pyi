from typing import Any, Literal


class dataAcquision:
    """Create the structured plant-pathology prompt for the vision workflow.

    This class converts field telemetry and farmer observations into the
    detailed instruction sent with an image to the Gemini-based vision model.
    Its prompt requests disease-management advice as a fixed JSON structure.
    """

    def __init__(self) -> None:
        """Initialize the cached prompt value.

        The instance starts with ``prompt`` unset until ``allFields`` receives
        valid crop data. This method accepts no parameters and returns ``None``.
        """
        ...

    def allFields(
        self, location: Any, crop_season: Any, temperature: Any, humidity: Any,
        rainfall: Any, windspeed: Any, variety: Any, irrigation: Any, soil: Any,
        symptoms: Any,
    ) -> str | Literal[False]:
        """Build the crop-disease analysis prompt from submitted field data.

        Args:
            location (Any): Required region or district of the field.
            crop_season (Any): Required growing season.
            temperature (Any): Required non-``None`` ambient-temperature value.
            humidity (Any): Required non-``None`` relative-humidity value.
            rainfall (Any): Required non-``None`` precipitation value.
            windspeed (Any): Required non-``None`` wind-speed value.
            variety (Any): Required crop cultivar or variety.
            irrigation (Any): Required irrigation method.
            soil (Any): Required soil type or description.
            symptoms (Any): Observed crop symptoms included in the prompt.

        Returns:
            str | Literal[False]: The fully formatted prompt and cached
            ``prompt`` value when required data is present; otherwise ``False``.
        """
        ...
