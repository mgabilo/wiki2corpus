<?php
  // 2009 Michael Gabilondo
  // Contents of "url.re" found in
  // http://immike.net/blog/2007/04/06/5-regular-expressions-every-web-programmer-should-know/
  $url_regex_file = fopen("url.re", 'r');
  $url_re = fread($url_regex_file, filesize("url.re"));
  fclose($url_regex_file);

  $stdin = fopen("php://stdin", 'r');
  while ($line = fgets($stdin)) {
      echo(preg_replace( $url_re, '-URL-', $line ));
  }
?>
