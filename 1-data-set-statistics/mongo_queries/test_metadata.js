//db.getCollection("test_metadata").find().limit(1)
//db.getCollection("test_metadata").count({ "video.comments": { $exists: true , $ne: null} })
//db.getCollection("test_metadata").count({ "video.comments": { $exists: true , $ne: null} })

//db.getCollection("test_metadata").aggregate([
//    {
//        "$group": {
//            _id: null,
//            "total": {
//                "$sum": {
//                    "$toInt": "$video.duration"
//                }
//            }
//        }
//    }
//])

//db.getCollection("test_metadata").aggregate([
//    {
//        "$group": {
//            _id: null,
//            "total": {
//                "$sum": {
//                    "$toLong": "$video.file.size"
//                }
//            }
//        }
//    }
//])

