document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM loaded")
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
            const {latitude, longitude} = position.coords;
            // const longitude = position.coords;
            console.log(`Position in latitude ${latitude} and ${longitude}`)
        },
        (error) => {
            console.error("Location permission/error:", error.message);
        }
      );
    }
  });


  const fileInput = document.getElementById('fileInput');
  const uploadForm = document.getElementById('uploadForm');
  const fileNameSpan = document.getElementById('filename');
  const dragNdrop = document.getElementById('dragNdrop');
  const warning = document.getElementById('warning');

  let selectedFile = null;

  function updateFileInfo(file) {
    if (file) {
      selectedFile = file;
      warning.classList.remove('display_block');
      fileNameSpan.textContent = `Selected File: ${file.name}`;
      console.log(file.name);
    }
  }

  uploadForm.addEventListener('submit', (e) => {
    if (!selectedFile) {
      e.preventDefault();
      warning.classList.add('display_block');
      console.log("Select a file first then submit");
    }
  });
  
  fileInput.addEventListener('change', (event) => {
    if (event.target.files && event.target.files.length > 0) {
      updateFileInfo(event.target.files[0]);
    }
  });
  
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dragNdrop.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
    }, false);
  });
  
  ['dragenter', 'dragover'].forEach(eventName => {
    dragNdrop.addEventListener(eventName, () => dragNdrop.classList.add('highlight'), false);
  });
  
  ['dragleave', 'drop'].forEach(eventName => {
    dragNdrop.addEventListener(eventName, () => dragNdrop.classList.remove('highlight'), false);
  });
  
  dragNdrop.addEventListener('drop', (e) => {
    const droppedFiles = e.dataTransfer.files;
    if (droppedFiles && droppedFiles.length > 0) {
      fileInput.files = droppedFiles; 
      updateFileInfo(droppedFiles[0]);
    }
  });
  
  uploadForm.addEventListener('reset', () => {
    selectedFile = null;
    fileNameSpan.textContent = 'Selected File: None';
    warning.classList.remove('display_block');
  });