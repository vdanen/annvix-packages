<?php
	if($_SERVER['argc']<2) die('Usage: '.$_SERVER['argv'][0].' <file> <path to remove>');
	$reg=unserialize(join('',file($_SERVER['argv'][1])));
	function clean($a, $path){
		if(is_string($a)) return str_replace($path, "", $a);
		if(is_array($a)){
			$aclean = Array();
			foreach($a as $k=>$v){
				$aclean[str_replace($path, "", $k)]=clean($v, $path);
			}
			return $aclean;
		}
		return $a;
	}

	$f = fopen($_SERVER['argv'][1], 'w');
	fputs($f, serialize(clean($reg, $_SERVER['argv'][2])));
	fclose($f);
?>
