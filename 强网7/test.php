<?php
highlight_file(__FILE__);
class hello{
    public $hello;
    public $name;
    private $win;
    public function __construct()
    {
        $this->hello="ctfer";
        echo "</br>"."construct!!"."</br>";
    }

    public function __get($name)
    {
        echo "</br>"."get!!"."</br>";
        return $this->$name=$this->name[$name];
    }


    public function __destruct()
    {
        echo $this->hello;
    }
}
class ctf{
    public $ctf;
    public $name;


    public function __toString()//到call
    {
        echo "</br>"."tostring!!"."</br>";
        $this->ctf->couse($this->name);
        return "你不想搞事情吗？";
    }
}
class er{
    public $er;
    public $cmd;
    public function __call($name, $arguments)
        //name是couse，arguments是上面的name是个数组，而且数组的第一个元素也是数组
    {
        echo "</br>"."call!!"."</br>";
        if (isset($this->cmd))
        {
            die("不可以搞事情");
        }
        if ($this->er->win)   //到get
        {
             echo "asfrjkh";
            call_user_func($this->cmd,$arguments[0][$name]);

        }

    }
}


$data=@$_POST["data"];
if (isset($data)){
    @unserialize($data);
}