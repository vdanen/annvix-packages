<?php

/**
 * $xml contains the contents of an XML file and $xsl contains
 * the contents of an XSLT stylesheet
 */
/*
$args = array("/_xml" => $xml,
		"/_xsl" => $xsl);
*/
$xml="foo.xml";
$xsl="foo.xsl";

$xh = xslt_create();
$data = xslt_process($xh, $xml, $xsl, NULL);
echo $data;
xslt_free($xh);
?>

