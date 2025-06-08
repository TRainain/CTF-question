<?php
// 数据库连接参数
$servername = "127.0.0.1";
$username = "root";
$password = "root";
$dbname = "dkctf";

// 创建数据库连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接是否成功
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 从表单获取数据
$username = $_POST['username'];
$password = $_POST['password'];


if(!isset($username)||!isset($password)||$username==''||$password==''){
    echo "帐号或密码不能为空！";
    die();
}
if($username == 'admin'||$username == 'Infernity'){
    die("该用户已存在！");
}
// 准备SQL语句并绑定参数
$stmt = $conn->prepare("INSERT INTO user (username, password) VALUES (?, ?)");
$stmt->bind_param("ss", $username, $password);

// 执行SQL语句
if ($stmt->execute()) {
    echo "注册成功！";
} else {
    echo "注册失败！";
}

// 关闭连接
$stmt->close();
$conn->close();
?>
