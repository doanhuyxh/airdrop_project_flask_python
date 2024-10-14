async function uploadFile(file_element) {
    const files = document.getElementById(`${file_element}`).files;
    const formData = new FormData();
    formData.append('file', files[0]);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();

    if (result.code == 200) {
        return result.file_path;
    } else {
        return result.message;
    }


}

function removeVietnameseTones(str) {
    str = str.normalize('NFD').replace(/[\u0300-\u036f]/g, ""); // Loại bỏ dấu
    str = str.replace(/đ/g, 'd').replace(/Đ/g, 'D'); // Chuyển đổi 'đ' và 'Đ'
    return str;
}

const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.onmouseenter = Swal.stopTimer;
        toast.onmouseleave = Swal.resumeTimer;
    }
});
