schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "gid": {
      "type": "integer"
    },
    "uid": {
      "type": "string"
    },
    "item": {
      "type": "object",
      "properties": {
        "nutrition_subgroup": {
          "type": "string"
        },
        "food_type": {
          "type": "string"
        },
        "description": {
          "type": "string"
        }
      },
      "required": [
        "nutrition_subgroup",
        "food_type",
        "description"
      ]
    },
    "metrics": {
      "type": "object",
      "properties": {
        "weight": {
          "type": "integer"
        },
        "unit": {
          "type": "string"
        },
        "ingredients": {
          "type": "array",
          "items": {}
        }
      },
      "required": [
        "weight",
        "unit"
      ]
    },
    "model": {
      "type": "object",
      "properties": {
        "project_name": {
          "type": "string"
        },
        "rgbd_file_names": {
          "type": "array",
          "items": [
            {
              "type": "string"
            }
          ]
        },
        "nutrition_facts_sources": {
          "type": "array",
          "items": [
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            }
          ]
        },
        "texture_sources": {
          "type": "array",
          "items": [
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            },
            {
              "type": "string"
            }
          ]
        },
        "quality": {
          "type": "integer"
        },
        "quality_comments": {
          "type": "string"
        }
      },
      "required": [
        "project_name",
        "rgbd_file_names",
      ]
    },
    "time": {
      "type": "object",
      "properties": {
        "started": {
          "type": "string"
        },
        "finished": {
          "type": "string"
        }
      },
      "required": [
      ]
    }
  },
  "required": [
    "gid",
    "uid",
    "item",
    "metrics",
    "model",
    "time"
  ]
}