<?php
// 定义将16进制转换为字符串的函数
function Hex2String($hex){
    $string = '';
    for ($i = 0; $i < strlen($hex) - 1; $i += 2) {
        $string .= chr(hexdec($hex[$i] . $hex[$i + 1]));
    }
    return $string;
}

// 尝试从cookie获取TOKEN，进行解码和验证
if(isset($_COOKIE['TOKEN'])) {
    $token = $_COOKIE['TOKEN'];
    $json_information = base64_decode(Hex2String($token));
    $information = json_decode($json_information, true);

    // 检查是否为admin用户
    if ($information['is_admin'] != 1) {
        die("you are not admin!!!");
    }
} else {
    // 如果没有TOKEN或者TOKEN不正确，则阻止访问
    die("No valid token provided!");
}

// 如果验证通过，则显示页面内容
?>
<!DOCTYPE html>
<html>
<style>
    .centered-text {
        text-align: center; /* 文本居中 */
        font-size: 35px; 
    }
    .seached-text {
        text-align: center; /* 文本居中 */
        font-size: 30px; 
    }
</style>
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <link rel="stylesheet" href="style.css">
    <title>一个没用的搜索引擎</title>
</head>
<div class="centered-text">
    Infernity最近写了一个意义不明的搜索引擎，说是可以根据你的账户名输出你的密码？
</div>
<div class="seached-text">
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

$username = $information['username'];
$md5_token = $information['token'];
if($md5_token !== md5($username)){
    die("用户名你自己改了吧？不可以坏坏哦！");
}
if(preg_match("/`|~|!|@|%|\^|&|-|\+|\[|\]|\{|\}|\||\\|\;|\:|\"|\<|\>|\?| |--|&&|<>|xor|case|when|if|benchmark|sleep|not|union|order|by|concat|group|is|rlike|offset|distinct|perpare|declare|left|mid|right|handler|set|char|hex|updatexml|0x7e|extractvalue|regexp|floor|having|between|into|join|file|outfile|load_file|create|drop|convert|cast|show|pg_sleep|reverse|execute|open|read|first|end|then|iconv|greatest/i",$username)){
    die("Hacker!!");
}

$sql = "SELECT password FROM user WHERE username = '$username'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // 因为我们假设用户名是唯一的，所以只取第一行结果
    $row = $result->fetch_assoc();
    echo "账户".$username."的密码是：</br>".$row['password'];
} else {
    echo "No user found.";
}
?>
</div>
</html>
