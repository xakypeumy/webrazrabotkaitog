document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const progressVar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');

    // перетаскивание
    dropZone.addEventListener('dragover', (e) => {
       e.preventDefault();
       dropZone.style.borderColor = '#007bff';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = '#ccc'
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#ccc';
        handleFiles(e.dataTransfer.files);
    });

    // выбор через кнопку
    document.querySelector('.choose-files-btn').addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
       handleFiles(e.target.files);
    });

    function handleFiles(files) {
        if (files.length === 0) return;
        document.querySelector('.upload-progress').style.display = 'block';
        const formData.append('files[]', file);
        for (let file of files) {
            formData.append('files[]', file);
        }

        fetch('/Uploads', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            showSuccessMessage(data);
        })
        .catch(error => {
            showErrorMessage(error);
        });

        formData.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percent = (e.loaded / e.total) * 100;
                progressBar.style.width = `${percent}%`;
                progressText.textContent = `${percent.toFixed(2)}% загружено`;
            }
        });

        formData.addEventListener('load', () => {
            progressBar.style.width = '100%';
            progressText.textContent = 'Загрузка завершена!';
        });
    }

    function showSuccessMessage(data) {
        alert('Файл успешно загружен!');

    }

    function showErrorMessage(error) {
        alert('При загрузке файла произошла ошибка');
        console.error(error);
    }
});