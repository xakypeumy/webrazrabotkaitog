```javascript
document.querySelector('.dropzone')?.addEventListener('click',()=>{
    document.querySelector('input[type=file]').click();
});