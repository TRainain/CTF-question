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

$username = $_POST["username"];
$password = $_POST["password"];

if(!isset($username)||!isset($password)||$username==''||$password==''){
    echo "帐号或密码不能为空！";
    die();
}

// 准备一个预处理语句
$stmt = $conn->prepare("SELECT * FROM user WHERE username = ?");
$stmt->bind_param("s", $username); // 's' 表示参数类型是字符串
$stmt->execute();     // 执行查询
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();     //从数据库拿密码
    $sqlpassword = $row['password'];
}

if($password === $sqlpassword){
    $md5_token = md5($username);
    $token0 = "{\"username\":\"$username\", \"token\":\"$md5_token\", \"is_admin\":0}";
    $token1 = bin2hex(base64_encode($token0));
    setcookie("TOKEN",$token1);
    header("location:/home.php");
}else{
    echo "帐号或密码错误";
}

// 关闭数据库连接
$conn->close();
?>
