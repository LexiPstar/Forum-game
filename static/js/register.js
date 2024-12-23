function bindEmailCaptchaClick() {
    $("#captcha-btn").click(function(event) {
        // $(this) 代表当前按钮的 jQuery 对象
        var $this = $(this);
        // 阻止默认事件（例如表单提交）
        event.preventDefault();

        var email = $("input[name='email']").val();
        $.ajax({
            url: "/author/captcha/email?email=" + email,
            method: 'GET',
            success: function(result) {
                console.log("服务器返回的数据：", result); // 打印服务器返回的结果
                var code = result['code'];
                if (code === 200) {
                    var countdown = 60; // 设置倒计时 60 秒
                    // 在倒计时开始前禁用按钮
                    $this.off('click');
                    var timer = setInterval(function() {
                        $this.text(countdown); // 更新按钮上的倒计时
                        countdown--;
                        // 倒计时结束时恢复按钮
                        if (countdown <= 0) {
                            clearInterval(timer); // 停止定时器
                            $this.text('获取验证码'); // 恢复按钮文字
                            // 倒计时结束后重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                } else {
                    // 如果返回的 code 不为 200，显示错误消息
                    alert(result['message'] || "验证码发送失败！");
                }
            },
            error: function(xhr, status, error) {
                // 处理 AJAX 请求失败的情况
                console.log("AJAX 错误: ", error);
                alert("请求失败，请稍后再试！");
            }
        });
    });
}

// 页面加载完成后执行
$(function() {
    bindEmailCaptchaClick();
});
