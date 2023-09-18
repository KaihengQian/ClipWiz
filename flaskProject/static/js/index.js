function handleDrop(event) {
    event.preventDefault();
    const files = event.dataTransfer.files;
    handleFiles(files);
}

function handleDragOver(event) {
    event.preventDefault();
}

function handleFileSelect(event) {
    const files = event.target.files;
    handleFiles(files);
}

function handleFiles(files) {
    const fileList = document.getElementById("fileList");

    for (const file of files) {
        const listItem = document.createElement("li");
        listItem.textContent = file.name;
        fileList.appendChild(listItem);
    }
}

function uploadFiles() {
    // Here you can implement the file upload logic
    // For demonstration, we're just displaying an alert with the selected file names
    const fileNames = selectedFiles.map(file => file.name).join(", ");
    alert(`Uploading files: ${fileNames}`);
}

function showMessage(message) {
  alert(message);
}

function submitForm(formId) {
  const form = document.getElementById(formId);
  const formData = new FormData(form);

  fetch(form.action, {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    showMessage(data.message);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function uploadFile(formId) {
  const form = document.getElementById(formId);
  const formData = new FormData(form);

  fetch(form.action, {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    showMessage(data.message);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}


// document.addEventListener('DOMContentLoaded', function () {
//     const processButton = document.getElementById('processButton');
//
//     processButton.addEventListener('click', function () {
//         // 显示加载中页面
//         // window.location.href="/loading";
//         // console.log("successful")
//
//         // 触发后端数据处理
//         fetch('/danmu', {
//             method: 'POST'
//         })
//         .then(response => {
//             if (response.ok) {
//                 return response.text();
//             } else {
//                 throw new Error('Data processing failed');
//             }
//         })
//         .then(data => {
//             // 可以在处理完成后执行其他操作，例如显示结果或跳转到其他页面
//             console.log(data);
//         })
//         .catch(error => {
//             console.error(error);
//         });
//     });
// });
