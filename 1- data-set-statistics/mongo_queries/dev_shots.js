// db.getCollection("dev_shots").find().limit(1)
//db.getCollection("dev_shots").count()

//db.getCollection("dev_shots").count({ "Segmentation.Segments.Segment": { $exists: true , $eq: []} })

//db.getCollection("dev_shots").aggregate([
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
