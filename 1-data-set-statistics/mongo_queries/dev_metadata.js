//db.getCollection("dev_metadata").find().limit(1)
//db.getCollection("dev_metadata").count({ "video.comments": { $exists: true , $ne: null} })
//db.getCollection("dev_metadata").count({ "video.comments": { $exists: true , $ne: null} })

//db.getCollection("dev_metadata").aggregate([
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

//db.getCollection("dev_metadata").aggregate([
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

