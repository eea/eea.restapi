""" visualization module """
import re
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import queryMultiAdapter


def getVisualizationLayout(chartData):
    """Get visualization layout with no data"""
    if not chartData or not chartData.get("data"):
        return None

    newData = chartData.get("data")

    for traceIndex, trace in enumerate(newData):
        for tk in trace:
            originalColumn = re.sub("src$", "", tk)
            if tk.endswith("src") and originalColumn in trace:
                newData[traceIndex][originalColumn] = []
        if not trace.get("transforms"):
            continue
        for transformIndex, _ in enumerate(trace.get("transforms")):
            newData[traceIndex]["transforms"][transformIndex]["target"] = []

    chartData["data"] = newData

    return chartData


class VisualizationGet(Service):
    """Get visualization data + layout"""

    def reply(self):
        """reply"""

        res = {
            "@id": self.context.absolute_url() + "#visualization",
            "visualization": {},
        }

        serializer = queryMultiAdapter(
            (self.context, self.request), ISerializeToJson
        )

        if serializer is None:
            self.request.response.setStatus(501)

            return dict(error=dict(message="No serializer available."))

        ser = serializer(version=self.request.get("version"))
        res["visualization"] = {
            "chartData": ser["visualization"]["chartData"],
            "provider_url": ser["visualization"]["provider_url"],
        }

        return res


class VisualizationLayoutGet(Service):
    """Get visualization layout"""

    def reply(self):
        """reply"""

        res = {
            "@id": self.context.absolute_url() + "#visualization-layout",
        }

        serializer = queryMultiAdapter(
            (self.context, self.request), ISerializeToJson
        )

        if serializer is None:
            self.request.response.setStatus(501)

            return dict(error=dict(message="No serializer available."))

        ser = serializer(version=self.request.get("version"))

        if not ser["visualization"]:
            return res

        res["visualization"] = {
            "chartData": getVisualizationLayout(
                ser["visualization"].get("chartData")
            ),
            "provider_url": ser["visualization"].get("provider_url"),
        }

        return res