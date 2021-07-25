class BasicChip extends X6.Node {};

BasicChip.config({
    width: 100,
    height: 100,
    markup: [{
            tagName: "rect",
            selector: "body",
        },
        // label
        {
            tagName: "text",
            selector: "label",
        },
        // FabricLatency
        {
            tagName: "rect",
            selector: "minLatFabric",
        },
        {
            tagName: "rect",
            selector: "avgLatFabric",
        },
        {
            tagName: "rect",
            selector: "maxLatFabric",
        },
        // LineLatency
        {
            tagName: "rect",
            selector: "minLatLine",
        },
        {
            tagName: "rect",
            selector: "avgLatLine",
        },
        {
            tagName: "rect",
            selector: "maxLatLine",
        },
        // Buffer
        {
            tagName: "rect",
            selector: "bufferContanier",
        },
        {
            tagName: "rect",
            selector: "bufferLine",
        },
    ],
    attrs: {
        body: {
            width: 100,
            height: 100,
            rx: 5,
            ry: 5,
            fill: "wheat",
            stroke: "black",
            strokeWidth: 0.8,
            // filter: {
            //     name: 'dropShadow',
            //     args: {
            //         dx: 3,
            //         dy: 3,
            //         blur: 3,
            //     },
            // },
        },
        label: {
            x: 27,
            y: 22.5,
            text: "N660",
            "font-family": "Verdana",
            "font-size": 15,
            textLength: 4,
            "text-anchor": "middle"
        },
        minLatFabric: {
            width: 12,
            height: 12,
            x: 54,
            y: 10,
            fill: "lightcyan",
            stroke: "black",
            strokeWidth: 0.5,
        },
        avgLatFabric: {
            width: 12,
            height: 12,
            x: 66,
            y: 10,
            fill: "lightcyan",
            stroke: "black",
            strokeWidth: 0.5,
        },
        maxLatFabric: {
            width: 12,
            height: 12,
            x: 78,
            y: 10,
            fill: "lightcyan",
            stroke: "black",
            strokeWidth: 0.5,
        },
        minLatLine: {
            width: 12,
            height: 12,
            x: 10,
            y: 78,
            fill: "lightcyan",
            stroke: "black",
            strokeWidth: 0.5,
        },
        avgLatLine: {
            width: 12,
            height: 12,
            x: 22,
            y: 78,
            fill: "yellow",
            stroke: "black",
            strokeWidth: 0.5,
        },
        maxLatLine: {
            width: 12,
            height: 12,
            x: 34,
            y: 78,
            fill: "red",
            stroke: "black",
            strokeWidth: 0.5,
        },
        bufferContanier: {
            width: 36,
            height: 60,
            x: 54,
            y: 30,
            fill: "white",
            stroke: "black",
            strokeWidth: 0.5,
        },
        bufferLine: {
            width: 36,
            height: 20,
            x: 54,
            y: 70,
            fill: "green",
            stroke: "black",
            strokeWidth: 0,
        }
    },
});


X6.Graph.registerNode("basic-chip", BasicChip);