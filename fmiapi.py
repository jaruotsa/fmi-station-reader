import requests

import xml.etree.ElementTree as ET

FMI_XML_NAMESPACES = {
    'wfs'   : 'http://www.opengis.net/wfs/2.0',
    'gml'   : 'http://www.opengis.net/gml/3.2',
    'BsWfs' : 'http://xml.fmi.fi/schema/wfs/2.0'
}

def get_fmi_url(api_key):
    """Get base URL for FMI service. Return None if api_key is missing."""
    if api_key:
        return 'http://data.fmi.fi/fmi-apikey/%s/wfs' % api_key

def getresponse(url, params):
    if(url and params):
        return requests.get(url, params=params)
    return None

def fmi_observations_weather_simple(api_key, params):
    """
    Get realtime information from finnish weather stations.
    """
    url = get_fmi_url(api_key)
    response = getresponse(url, params)
    if response:
        results = {}
        root = ET.fromstring(response.text)
        ns = FMI_XML_NAMESPACES
        for elem in root.iterfind('.//BsWfs:BsWfsElement', ns):
            time = elem.find('.//BsWfs:Time', ns).text
            name = elem.find('.//BsWfs:ParameterName', ns).text
            value = elem.find('.//BsWfs:ParameterValue', ns).text

            measuretime = results.get(time)
            if measuretime:
                parameter = measuretime.get(name)
                if parameter:
                    print "ERROR: Duplicate value for parameter:", name  
                else:
                    measuretime[name] = value
            else:
                results[time] = { name : value }
        
        return results
    else:
        print 'ERROR: Could not get data from FMI API.'
