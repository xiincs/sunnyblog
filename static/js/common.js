const loginUrl = "/login";
$(document).ready(function () {
    $('#loginform').submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: loginUrl,
            data: $(this).serialize(),
            success: function (response) {
                console.log(response);  // 检查响应
                if (response.status === "success") {
                    console.log("Refreshing page...");  // 检查条件判断
                    window.location.reload();  // 使用 window.location.reload()
                } else {
                    $('#status').text(response.status);
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX error:", status, error);  // 捕获 AJAX 错误
            }
        });
    });
});
