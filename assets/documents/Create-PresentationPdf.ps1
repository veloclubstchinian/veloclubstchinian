$outPath = 'C:\Users\TEMP\Desktop\site velo\assets\documents\Velo-Club-Saint-Chinianais-Presentation.pdf'

$streamText = @"
BT
/F1 18 Tf
72 720 Td
(Velo-Club Saint-Chinianais) Tj
0 -22 Td
(Passion VTT, nature, apprentissage et convivialite) Tj
0 -22 Td
(Ecole de VTT FFC, parcours VTT-FFC N199) Tj
0 -22 Td
(Competition, sport-sante et vie locale) Tj
ET
"@

$streamBytes = [System.Text.Encoding]::ASCII.GetBytes($streamText)
$streamLength = $streamBytes.Length

$objects = @(
    '1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj',
    '2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj',
    '3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>endobj',
    ("4 0 obj<< /Length $streamLength >>stream`r`n" + $streamText + "`r`nendstream`r`nendobj"),
    '5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj'
)

$pdfBytes = [System.Text.Encoding]::ASCII.GetBytes('%PDF-1.4' + "`r`n")
$offsets = @(0)
foreach ($obj in $objects) {
    $offsets += $pdfBytes.Length
    $pdfBytes += [System.Text.Encoding]::ASCII.GetBytes($obj + "`r`n")
}

$xrefOffset = $pdfBytes.Length
$xref = "xref`r`n0 $($objects.Count + 1)`r`n0000000000 65535 f `r`n"
for ($i = 1; $i -lt $offsets.Length; $i++) {
    $xref += ('{0:D10}' -f $offsets[$i]) + ' 00000 n `r`n'
}

$pdfBytes += [System.Text.Encoding]::ASCII.GetBytes($xref)
$pdfBytes += [System.Text.Encoding]::ASCII.GetBytes("trailer<< /Root 1 0 R /Size $($objects.Count + 1) >>`r`nstartxref $xrefOffset`r`n%%EOF`r`n")

[System.IO.File]::WriteAllBytes($outPath, $pdfBytes)
Write-Host "PDF_OK $outPath"
Get-Item $outPath | Select-Object Name, Length, FullName
