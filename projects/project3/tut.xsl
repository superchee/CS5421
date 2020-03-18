<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:template match="/">
    <html>
      <body>
        <xsl:apply-templates select="library/album[genres/genre='Pop']"/>
      </body>
    </html>
  </xsl:template>
  <xsl:template match="album">
    <h2>
      Album <xsl:value-of select="title"/> - <xsl:value-of select="year"/>
    </h2>
  </xsl:template>
</xsl:stylesheet>
