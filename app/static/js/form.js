const dropzone = document.getElementById('dropzone');
const images = document.getElementById('images');
const previews = document.getElementById('dz-previews');
var img_files = [];

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults (e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropzone.classList.add('highlight');
}

function unhighlight(e) {
    dropzone.classList.remove('highlight');
}

function uploadFile(file) {
    img_files = [...img_files, file];
}

function previewFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function() {
        let div = document.createElement('div');
        let icon = document.createElement('i');
        let img = document.createElement('img');
        icon.className = "fa fa-times";
        img.src = reader.result;
        img.id = file.name;
        img.draggable = false;
        img.ondragstart = 'return false';
        div.appendChild(icon);
        div.appendChild(img);
        previews.appendChild(div);
    }
}

function handleFiles(files) {
    [...files].forEach((f) => {
        if (!img_files.some(img => img.name === f.name)) {
            uploadFile(f);
            previewFile(f);
        }
    });
    let dt = new DataTransfer();
    img_files.forEach((f) => {
        dt.items.add(f);
    });
    images.files = dt.files;
}

dropzone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    console.log(e.dataTransfer.files);
    if (e.dataTransfer.files.length > 0) {
        let files = e.dataTransfer.files;
        handleFiles(files)
    }
}
