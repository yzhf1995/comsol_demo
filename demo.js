const data = {
    // 节点
    nodes: [{
            id: 'node1', // String，可选，节点的唯一标识
            x: 40, // Number，必选，节点位置的 x 值
            y: 40, // Number，必选，节点位置的 y 值
            label: 'hello', // String，节点标签
            shape: 'basic-chip',
        },
        {
            id: 'node2', // String，节点的唯一标识
            x: 160, // Number，必选，节点位置的 x 值
            y: 180, // Number，必选，节点位置的 y 值
            label: 'world', // String，节点标签
            shape: 'basic-chip',
        },
    ],
    // 边
    edges: [{
        source: 'node1', // String，必须，起始节点 id
        target: 'node2', // String，必须，目标节点 id
    }, ],
};

// 使用 CDN 引入时暴露了 X6 全局变量
// const { Graph } = X6

const graph = new X6.Graph({
    container: document.getElementById('x6-top'),
    width: 2560,
    height: 1920,
});

graph.fromJSON(data)