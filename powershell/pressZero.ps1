Add-Type -AssemblyName PresentationCore, WindowsBase

$sleepTime = 200000

$stopKey = 'END'

while ($true)
{

      if([System.Windows.Input.Keyboard]::IsKeyDown($stopKey)){
           Write-Host "stop."
           break
       }
	
        $wshell = New-Object -ComObject wscript.shell

        Write-Host "1."

        $wshell.SendKeys('0') 
	
        Start-Sleep -Milliseconds $sleepTime

}
