<?xml version='1.0' ?>
<xsl:stylesheet id="stylesheet" version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">


<xsl:template match="warehouse">
        <tr>
        	<xsl:apply-templates select="name"/>
        	<xsl:apply-templates select="items/item[1]/name"/>

        </tr>
</xsl:template>

<xsl:template match="name">
          <td><xsl:value-of select="."/></td>
</xsl:template>

<xsl:template match="items/item[1]/name">
          <td><xsl:value-of select="."/></td>
</xsl:template>

<xsl:template match="/">
  <html>
  <body>
    <table border="1">
      <tr>
        <th>name of warehouse</th>
        <th>name of item with largest quantity</th>
      </tr>
      <xsl:apply-templates select="/warehouses/warehouse[address/country = 'Singapore' or address/country = 'Malaysia']"/>
    </table>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>