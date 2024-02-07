document.addEventListener('DOMContentLoaded', function() {
    // 게시글 삭제
    function deleteNotice() {

        if (confirm("정말로 삭제하시겠습니까?")) {
            var xhr = new XMLHttpRequest();
            var id = document.getElementById("delete-btn").getAttribute("data-id");
            var csrfToken = getCookie('csrftoken');
            
            
            xhr.open("POST", "/main/notice/view/delete/" + id + "/");
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.setRequestHeader('X-CSRFToken', csrfToken);

            xhr.onload = function() {
                if (xhr.status === 200)  // 삭제 성공
                    location.href = "/main/notice/";
                else { // 삭제 실패
                    alert("이미 삭제된 게시글 입니다");
                }
            };
            xhr.send();
        }
    }

    document.getElementById("delete-btn").addEventListener("click", deleteNotice);
});