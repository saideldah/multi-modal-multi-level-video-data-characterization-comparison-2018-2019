//db.getCollection("test_shots").find().limit(1)
//db.getCollection("test_shots").count()

//db.getCollection("test_shots").count({ "Segmentation.Segments.Segment": { $exists: false} })

//total number of shots
//db.getCollection("test_shots").aggregate([
//    {
//        $group: {
//            _id: null,
//            "total_segments": {
//                $sum: {
//                    $cond: {
//                        if: { $isArray: "$Segmentation.Segments.Segment" },
//                        then: { $size: "$Segmentation.Segments.Segment" },
//                        else: 1
//                    }
//                }
//            }
//        }
//    }
//])


db.dev_shots.aggregate([
    {
        $project: {
            "segments": "$Segmentation.Segments.Segment"
        }
    },
    {
        $match:
            {
                "segments": { $exists: true }
            }
    },
    {
        $unwind: "$segments"
    },
    {
        $project: {
            _id: 0,
            start: "$segments.@start",
            end: "$segments.@end",
            duration: "$segments.duration"
        }
    },
    {
        $match: {
            "duration": { $gt: 2 }
        }
    },
    {
        $group:
            {
                _id: 0,
                maxDuration: { $max: "$duration" }
            }
    }
]);
