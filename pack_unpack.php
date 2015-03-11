<?php

$s="6566";
$str=pack("H*",$s);//对16进制流打包
var_dump($str);//ef

$s="ef";
$str=unpack("H*",$s);//解包为16进制
var_dump($str);//6566
