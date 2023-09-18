document.addEventListener('DOMContentLoaded', function () {
    // 发起后端数据处理请求
    fetch('/soccer', {
        method: 'POST'
    })
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Data processing failed');
            }
        })
        .then(data => {
            // 在数据处理完成后，可以在这里执行其他操作，例如跳转到结果页面或显示处理结果
            console.log(data);
            window.close();
        })
        .catch(error => {
            console.error(error);
        });
});