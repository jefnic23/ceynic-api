const price = document.getElementById('price');
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
        div.className = "preview";
        icon.className = "fa fa-times-circle-o close";
        icon.ariaHidden = "true";
        icon.setAttribute('onclick', 'removeImage(this)');
        img.src = reader.result;
        img.id = file.name;
        img.className = "dz-img";
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
    setImages();
}

dropzone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    if (e.dataTransfer.files.length > 0) {
        let files = e.dataTransfer.files;
        handleFiles(files)
    }
}

function removeImage(e) {
    img_files = img_files.filter(img => img.name !== e.nextElementSibling.id);
    e.parentNode.remove();
    setImages();
}

function setImages() {
    let dt = new DataTransfer();
    img_files.forEach((f) => {
        dt.items.add(f);
    });
    images.files = dt.files;
}

function prefill(files) {
    [...files].forEach((file) => {
        createFile(file).then((f) => {
            if (!img_files.some(img => img.name === f.name)) {
                uploadFile(f);
                previewFile(f);
                setImages();
            }
        });
    });
}

async function createFile(e) {
    let fname = e.split('/').at(-1);
    let res = await fetch(e);
    let data = await res.blob();
    let metadata = {
        name: fname,
        type: 'image/*'
    };
    return file = new File([data], fname, metadata);
}

(function () {
    'use strict';
    let forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms)
        .forEach((form) => {
            form.addEventListener('submit', (event) => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
})()
