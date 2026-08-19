const locationInput = document.getElementById("location");

  locationInput.addEventListener("blur", async function () {
    const query = this.value.trim();
    if (!query) return;

    const tempField = document.getElementById("temperature");
    const humField = document.getElementById("humidity");
    const rainField = document.getElementById("rainfall");
    const windField = document.getElementById("windspeed");

    // Indicate loading state
    tempField.placeholder = "Loading...";
    humField.placeholder = "Loading...";
    rainField.placeholder = "Loading...";
    windField.placeholder = "Loading...";

    try {
      // 1. Forward Geocode via Nominatim API directly in browser
      const geoUrl = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=1`;
      const geoResponse = await fetch(geoUrl);
      const geoData = await geoResponse.json();

      if (!geoData || geoData.length === 0) {
        throw new Error("Location not found");
      }

      const lat = geoData[0].lat;
      const lon = geoData[0].lon;

      // 2. Fetch Weather via Open-Meteo API
      const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,rain,wind_speed_10m`;
      const weatherResponse = await fetch(weatherUrl);
      const weatherData = await weatherResponse.json();

      const current = weatherData.current;

      // 3. Populate Form Fields
      tempField.value = `${current.temperature_2m ?? "--"} °C`;
      humField.value = `${current.relative_humidity_2m ?? "--"} %`;
      rainField.value = `${current.rain ?? 0} mm`;
      windField.value = `${current.wind_speed_10m ?? "--"} km/h`;

    } catch (error) {
      console.error("Error fetching location/weather:", error);
      tempField.value = "";
      humField.value = "";
      rainField.value = "";
      windField.value = "";

      tempField.placeholder = "Location not found / error";
      humField.placeholder = "Location not found / error";
      rainField.placeholder = "Location not found / error";
      windField.placeholder = "Location not found / error";
    }
  });