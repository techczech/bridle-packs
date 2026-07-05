COMPLEX_HTML = """<!doctype html>
<html>
  <body>
    <table id="complex" data-title="Synthetic Archive Table">
      <caption>Synthetic Archive Table</caption>
      <thead>
        <tr>
          <th rowspan="2" colspan="2">Archive labels</th>
          <th colspan="2">Metrics</th>
          <th rowspan="2">Notes</th>
        </tr>
        <tr>
          <th>Count</th>
          <th>Share</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="2">Collection A</th>
          <th>Letters</th>
          <td>12</td>
          <td>0.60</td>
          <td>
            <ul>
              <li>catalogued</li>
              <li>needs review</li>
            </ul>
          </td>
        </tr>
        <tr>
          <th>Reports</th>
          <td colspan="2">Merged metric pending</td>
          <td>
            <table>
              <tr><th>Flag</th><th>Value</th></tr>
              <tr><td>quality</td><td>high</td></tr>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
  </body>
</html>
"""
