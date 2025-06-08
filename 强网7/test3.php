<?php
class Test {
    public $name = ['foo' => 'bar'];

    public function __get($name) {
        echo "</br>"."get!!"."</br>";
        return $this->$name = $this->name[$name];
    }
}

$obj = new Test();
echo $obj->baz; // 访问不存在的键 baz
$array =[['couse' => 'system'], ['ls']];
echo $array[0]["couse"];